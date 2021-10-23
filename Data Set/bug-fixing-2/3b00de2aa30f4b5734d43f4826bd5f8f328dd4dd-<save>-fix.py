

def save(self, project, raw=False):
    from sentry.tasks.post_process import index_event_tags
    project = Project.objects.get_from_cache(id=project)
    data = self.data.copy()
    event_id = data.pop('event_id')
    level = data.pop('level')
    culprit = data.pop('transaction', None)
    if (not culprit):
        culprit = data.pop('culprit', None)
    logger_name = data.pop('logger', None)
    server_name = data.pop('server_name', None)
    site = data.pop('site', None)
    checksum = data.pop('checksum', None)
    fingerprint = data.pop('fingerprint', None)
    platform = data.pop('platform', None)
    release = data.pop('release', None)
    dist = data.pop('dist', None)
    environment = data.pop('environment', None)
    time_spent = data.pop('time_spent', None)
    message = data.pop('message', '')
    if (not culprit):
        transaction_name = None
        culprit = generate_culprit(data, platform=platform)
    else:
        transaction_name = culprit
    culprit = force_text(culprit)
    recorded_timestamp = data.pop('timestamp')
    date = datetime.fromtimestamp(recorded_timestamp)
    date = date.replace(tzinfo=timezone.utc)
    kwargs = {
        'platform': platform,
    }
    event = Event(project_id=project.id, event_id=event_id, data=data, time_spent=time_spent, datetime=date, **kwargs)
    event._project_cache = project
    tags = dict((data.get('tags') or []))
    tags['level'] = LOG_LEVELS[level]
    if logger_name:
        tags['logger'] = logger_name
    if server_name:
        tags['server_name'] = server_name
    if site:
        tags['site'] = site
    if environment:
        tags['environment'] = environment
    if transaction_name:
        tags['transaction'] = transaction_name
    if release:
        if ('release' in tags):
            del tags['release']
        release = Release.get_or_create(project=project, version=release, date_added=date)
        tags['sentry:release'] = release.version
    if (dist and release):
        dist = release.add_dist(dist, date)
        tags['sentry:dist'] = dist.name
    else:
        dist = None
    event_user = self._get_event_user(project, data)
    if event_user:
        if ('user' in tags):
            del tags['user']
        tags['sentry:user'] = event_user.tag_value
    normalize_in_app(data)
    for plugin in plugins.for_project(project, version=None):
        added_tags = safe_execute(plugin.get_tags, event, _with_transaction=False)
        if added_tags:
            for (key, value) in added_tags:
                tags.setdefault(key, value)
    for (path, iface) in six.iteritems(event.interfaces):
        for (k, v) in iface.iter_tags():
            tags[k] = v
        if iface.ephemeral:
            data.pop(iface.get_path(), None)
    tags = tags.items()
    data['tags'] = tags
    data['fingerprint'] = (fingerprint or ['{{ default }}'])
    if fingerprint:
        hashes = [md5_from_hash(h) for h in get_hashes_from_fingerprint(event, fingerprint)]
    elif checksum:
        hashes = [checksum]
        data['checksum'] = checksum
    else:
        hashes = [md5_from_hash(h) for h in get_hashes_for_event(event)]
    data['message'] = message
    event_type = eventtypes.get(data.get('type', 'default'))(data)
    event_metadata = event_type.get_metadata()
    del data['message']
    data['type'] = event_type.key
    data['metadata'] = event_metadata
    if (event_type.key != 'default'):
        if (('sentry.interfaces.Message' in data) and (data['sentry.interfaces.Message']['message'] != message)):
            message = '{} {}'.format(message, data['sentry.interfaces.Message']['message'])
    if (not message):
        message = ''
    elif (not isinstance(message, six.string_types)):
        message = force_text(message)
    for value in six.itervalues(event_metadata):
        value_u = force_text(value, errors='replace')
        if (value_u not in message):
            message = '{} {}'.format(message, value_u)
    if (culprit and (culprit not in message)):
        culprit_u = force_text(culprit, errors='replace')
        message = '{} {}'.format(message, culprit_u)
    message = trim(message.strip(), settings.SENTRY_MAX_MESSAGE_LENGTH)
    event.message = message
    kwargs['message'] = message
    received_timestamp = (event.data.get('received') or float(event.datetime.strftime('%s')))
    group_kwargs = kwargs.copy()
    group_kwargs.update({
        'culprit': culprit,
        'logger': logger_name,
        'level': level,
        'last_seen': date,
        'first_seen': date,
        'active_at': date,
        'data': {
            'last_received': received_timestamp,
            'type': event_type.key,
            'metadata': event_metadata,
        },
    })
    if release:
        group_kwargs['first_release'] = release
    try:
        (group, is_new, is_regression, is_sample) = self._save_aggregate(event=event, hashes=hashes, release=release, **group_kwargs)
    except HashDiscarded:
        event_discarded.send_robust(project=project, sender=EventManager)
        metrics.incr('events.discarded', skip_internal=True, tags={
            'organization_id': project.organization_id,
            'platform': platform,
        })
        raise
    else:
        event_saved.send_robust(project=project, sender=EventManager)
    event.group = group
    event.data.bind_ref(event)
    if is_sample:
        try:
            with transaction.atomic(using=router.db_for_write(EventMapping)):
                EventMapping.objects.create(project=project, group=group, event_id=event_id)
        except IntegrityError:
            self.logger.info('duplicate.found', exc_info=True, extra={
                'event_uuid': event_id,
                'project_id': project.id,
                'group_id': group.id,
                'model': EventMapping.__name__,
            })
            return event
    if Event.objects.filter(project_id=project.id, event_id=event_id).exists():
        self.logger.info('duplicate.found', exc_info=True, extra={
            'event_uuid': event_id,
            'project_id': project.id,
            'group_id': group.id,
            'model': Event.__name__,
        })
        return event
    environment = Environment.get_or_create(project=project, name=environment)
    (group_environment, is_new_group_environment) = GroupEnvironment.get_or_create(group_id=group.id, environment_id=environment.id, defaults={
        'first_release_id': (release.id if release else None),
    })
    if release:
        ReleaseEnvironment.get_or_create(project=project, release=release, environment=environment, datetime=date)
        ReleaseProjectEnvironment.get_or_create(project=project, release=release, environment=environment, datetime=date)
        grouprelease = GroupRelease.get_or_create(group=group, release=release, environment=environment, datetime=date)
    counters = [(tsdb.models.group, group.id), (tsdb.models.project, project.id)]
    if release:
        counters.append((tsdb.models.release, release.id))
    tsdb.incr_multi(counters, timestamp=event.datetime, environment_id=environment.id)
    frequencies = [(tsdb.models.frequent_environments_by_group, {
        group.id: {
            environment.id: 1,
        },
    })]
    if release:
        frequencies.append((tsdb.models.frequent_releases_by_group, {
            group.id: {
                grouprelease.id: 1,
            },
        }))
    tsdb.record_frequency_multi(frequencies, timestamp=event.datetime)
    UserReport.objects.filter(project=project, event_id=event_id).update(group=group, environment=environment)
    if (not is_sample):
        try:
            with transaction.atomic(using=router.db_for_write(Event)):
                event.save()
        except IntegrityError:
            self.logger.info('duplicate.found', exc_info=True, extra={
                'event_uuid': event_id,
                'project_id': project.id,
                'group_id': group.id,
                'model': Event.__name__,
            })
            return event
        index_event_tags.delay(organization_id=project.organization_id, project_id=project.id, group_id=group.id, environment_id=environment.id, event_id=event.id, tags=tags)
    if event_user:
        tsdb.record_multi(((tsdb.models.users_affected_by_group, group.id, (event_user.tag_value,)), (tsdb.models.users_affected_by_project, project.id, (event_user.tag_value,))), timestamp=event.datetime, environment_id=environment.id)
    if release:
        if is_new:
            buffer.incr(ReleaseProject, {
                'new_groups': 1,
            }, {
                'release_id': release.id,
                'project_id': project.id,
            })
        if is_new_group_environment:
            buffer.incr(ReleaseProjectEnvironment, {
                'new_issues_count': 1,
            }, {
                'project_id': project.id,
                'release_id': release.id,
                'environment_id': environment.id,
            })
    safe_execute(Group.objects.add_tags, group, environment, tags, _with_transaction=False)
    if (not raw):
        if (not project.first_event):
            project.update(first_event=date)
            first_event_received.send(project=project, group=group, sender=Project)
        post_process_group.delay(group=group, event=event, is_new=is_new, is_sample=is_sample, is_regression=is_regression, is_new_group_environment=is_new_group_environment, primary_hash=hashes[0])
    else:
        self.logger.info('post_process.skip.raw_event', extra={
            'event_id': event.id,
        })
    if (is_regression and (not raw)):
        regression_signal.send_robust(sender=Group, instance=group)
    metrics.timing('events.latency', (received_timestamp - recorded_timestamp), tags={
        'project_id': project.id,
    })
    return event
