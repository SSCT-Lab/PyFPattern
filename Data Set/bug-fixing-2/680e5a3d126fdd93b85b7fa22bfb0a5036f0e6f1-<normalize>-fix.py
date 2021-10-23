

def normalize(self):
    if self._normalized:
        raise RuntimeError('Already normalized')
    self._normalized = True
    if ENABLE_RUST:
        from semaphore.processing import StoreNormalizer
        rust_normalizer = StoreNormalizer(geoip_lookup=rust_geoip, project_id=(self._project.id if self._project else None), client_ip=self._client_ip, client=(self._auth.client if self._auth else None), is_public_auth=(self._auth.is_public if self._auth else False), key_id=(six.text_type(self._key.id) if self._key else None), protocol_version=(six.text_type(self.version) if (self.version is not None) else None), stacktrace_frames_hard_limit=settings.SENTRY_STACKTRACE_FRAMES_HARD_LIMIT, max_stacktrace_frames=settings.SENTRY_MAX_STACKTRACE_FRAMES, valid_platforms=list(VALID_PLATFORMS), max_secs_in_future=MAX_SECS_IN_FUTURE, max_secs_in_past=MAX_SECS_IN_PAST, enable_trimming=ENABLE_TRIMMING)
        self._data = CanonicalKeyDict(rust_normalizer.normalize_event(dict(self._data)))
        normalize_user_agent(self._data)
        return
    data = self._data
    text = six.text_type

    def to_values(v):
        return ({
            'values': v,
        } if (v and isinstance(v, (tuple, list))) else v)
    casts = {
        'environment': (lambda v: (text(v) if (v is not None) else v)),
        'event_id': (lambda v: v.lower()),
        'fingerprint': cast_fingerprint,
        'release': (lambda v: (text(v) if (v is not None) else v)),
        'dist': (lambda v: (text(v).strip() if (v is not None) else v)),
        'time_spent': (lambda v: (int(v) if (v is not None) else v)),
        'tags': (lambda v: [(text(v_k).replace(' ', '-').strip(), text(v_v).strip()) for (v_k, v_v) in dict(v).items()]),
        'platform': (lambda v: (v if (v in VALID_PLATFORMS) else 'other')),
        'logentry': (lambda v: ({
            'message': v,
        } if (v and (not isinstance(v, dict))) else (v or None))),
        'exception': to_values,
        'breadcrumbs': to_values,
        'threads': to_values,
    }
    meta = Meta(data.get('_meta'))
    for c in casts:
        value = data.pop(c, None)
        if (value is not None):
            try:
                data[c] = casts[c](value)
            except Exception as e:
                meta.enter(c).add_error(EventError.INVALID_DATA, value, {
                    'reason': six.text_type(e),
                })
    data['timestamp'] = process_timestamp(data.get('timestamp'), meta.enter('timestamp'))
    if self._client_ip:
        if (get_path(data, 'request', 'env', 'REMOTE_ADDR') == '{{auto}}'):
            data['request']['env']['REMOTE_ADDR'] = self._client_ip
        if (get_path(data, 'user', 'ip_address') == '{{auto}}'):
            data['user']['ip_address'] = self._client_ip
    validate_and_default_interface(data.data, 'event', meta=meta)
    if (data.get('tags') is not None):
        validate_and_default_interface(data['tags'], 'tags', name='tags', meta=meta.enter('tags'))
    for k in list(iter(data)):
        if (k in CLIENT_RESERVED_ATTRS):
            continue
        value = data.pop(k)
        if ((not value) or (k in CLIENT_IGNORED_ATTRS)):
            continue
        try:
            interface = get_interface(k)
        except ValueError:
            logger.debug('Ignored unknown attribute: %s', k)
            meta.enter(k).add_error(EventError.INVALID_ATTRIBUTE)
            continue
        normalized = interface.normalize(value, meta.enter(k))
        if normalized:
            data[interface.path] = normalized
    if self._for_store:
        if (self._project is not None):
            data['project'] = self._project.id
        if (self._key is not None):
            data['key_id'] = self._key.id
        if (self._auth is not None):
            data['sdk'] = (data.get('sdk') or parse_client_as_sdk(self._auth.client))
        level = (data.get('level') or DEFAULT_LOG_LEVEL)
        if (isinstance(level, int) or (isinstance(level, six.string_types) and level.isdigit())):
            level = LOG_LEVELS.get(int(level), DEFAULT_LOG_LEVEL)
        if (level not in LOG_LEVELS_MAP):
            level = DEFAULT_LOG_LEVEL
        data['level'] = level
        if (data.get('dist') and (not data.get('release'))):
            data['dist'] = None
        timestamp = data.get('timestamp')
        if (not timestamp):
            timestamp = timezone.now()
        if isinstance(timestamp, datetime):
            if settings.TIME_ZONE:
                if (not timezone.is_aware(timestamp)):
                    timestamp = timestamp.replace(tzinfo=timezone.utc)
            elif timezone.is_aware(timestamp):
                timestamp = timestamp.replace(tzinfo=None)
            timestamp = float(timestamp.strftime('%s'))
        data['timestamp'] = timestamp
        data['received'] = float(timezone.now().strftime('%s'))
        setdefault_path(data, 'extra', value={
            
        })
        setdefault_path(data, 'logger', value=DEFAULT_LOGGER_NAME)
        setdefault_path(data, 'tags', value=[])
        if (not data.get('environment')):
            tagsdict = dict(data['tags'])
            if ('environment' in tagsdict):
                data['environment'] = tagsdict['environment']
                del tagsdict['environment']
                data['tags'] = tagsdict.items()
        data['type'] = eventtypes.infer(data).key
        data['version'] = self.version
    exceptions = get_path(data, 'exception', 'values', filter=True)
    stacktrace = data.get('stacktrace')
    if (stacktrace and exceptions and (len(exceptions) == 1)):
        exceptions[0]['stacktrace'] = stacktrace
        stacktrace_meta = meta.enter('stacktrace')
        meta.enter('exception', 'values', 0, 'stacktrace').merge(stacktrace_meta)
        del data['stacktrace']
    if exceptions:
        sdk_info = get_sdk_from_event(data)
        for ex in exceptions:
            if ('mechanism' in ex):
                normalize_mechanism_meta(ex['mechanism'], sdk_info)
    normalize_user_agent(data)
    if (not get_path(data, 'user', 'ip_address')):
        is_public = (self._auth and self._auth.is_public)
        add_ip_platforms = ('javascript', 'cocoa', 'objc')
        http_ip = get_path(data, 'request', 'env', 'REMOTE_ADDR')
        if http_ip:
            set_path(data, 'user', 'ip_address', value=http_ip)
        elif (self._client_ip and (is_public or (data.get('platform') in add_ip_platforms))):
            set_path(data, 'user', 'ip_address', value=self._client_ip)
    if data.get('logger'):
        data['logger'] = trim(data['logger'].strip(), 64)
    if data.get('extra'):
        trim_dict(data['extra'], max_size=settings.SENTRY_MAX_EXTRA_VARIABLE_SIZE)
    if data.get('culprit'):
        data['culprit'] = trim(data['culprit'], MAX_CULPRIT_LENGTH)
    if data.get('transaction'):
        data['transaction'] = trim(data['transaction'], MAX_CULPRIT_LENGTH)
    site = data.pop('site', None)
    if (site is not None):
        set_tag(data, 'site', site)
    server_name = data.pop('server_name', None)
    if (server_name is not None):
        set_tag(data, 'server_name', server_name)
    for key in ('fingerprint', 'modules', 'tags', 'extra', 'contexts'):
        if (not data.get(key)):
            data.pop(key, None)
    errors = (data.get('errors') or [])
    add_meta_errors(errors, meta)
    add_meta_errors(errors, meta.enter('tags'))
    if errors:
        data['errors'] = errors
    elif ('errors' in data):
        del data['errors']
    if meta.raw():
        data['_meta'] = meta.raw()
    elif ('_meta' in data):
        del data['_meta']
    self._data = CanonicalKeyDict(prune_empty_keys(data))
