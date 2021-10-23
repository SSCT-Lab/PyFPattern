def save(self, project_id, raw=False):
    from sentry.tasks.post_process import index_event_tags
    data = self._data
    project = Project.objects.get_from_cache(id=project_id)
    try:
        event = Event.objects.get(project_id=project.id, event_id=data['event_id'])
    except Event.DoesNotExist:
        pass
    else:
        logger.info('duplicate.found', exc_info=True, extra={
            'event_uuid': data['event_id'],
            'project_id': project.id,
            'model': Event.__name__,
        })
        return event
    level = data.pop('level')
    transaction_name = data.pop('transaction', None)
    culprit = data.pop('culprit', None)
    logger_name = data.pop('logger', None)
    server_name = data.pop('server_name', None)
    site = data.pop('site', None)
    checksum = data.pop('checksum', None)
    fingerprint = data.pop('fingerprint', None)
    release = data.pop('release', None)
    dist = data.pop('dist', None)
    environment = data.pop('environment', None)
    recorded_timestamp = data.get('timestamp')
    data.pop('message', None)
    event = self._get_event_instance(project_id=project_id)
    event._project_cache = project
    date = event.datetime
    platform = event.platform
    event_id = event.event_id
    data = event.data.data
    self._data = None
    culprit = (culprit or transaction_name or generate_culprit(data, platform=platform) or '')
    culprit = force_text(culprit)
    if transaction_name:
        transaction_name = force_text(transaction_name)
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
            data.pop(iface.path, None)
    tags = tags.items()
    data['tags'] = tags
    data['fingerprint'] = (fingerprint or ['{{ default }}'])
    if fingerprint:
        hashes = [md5_from_hash(h) for h in get_hashes_from_fingerprint(event, fingerprint)]
    elif checksum:
        if HASH_RE.match(checksum):
            hashes = [checksum]
        else:
            hashes = [md5_from_hash([checksum]), checksum]
        data['checksum'] = checksum
    else:
        hashes = [md5_from_hash(h) for h in get_hashes_for_event(event)]
    event_type = eventtypes.get(data.get('type', 'default'))(data)
    event_metadata = event_type.get_metadata()
    data['type'] = event_type.key
    data['metadata'] = event_metadata
    event.message = self.get_search_message(data, event_metadata, culprit)
    kwargs = {
        'platform': platform,
        'message': event.message,
    }
    received_timestamp = (event.data.get('received') or float(event.datetime.strftime('%s')))
    kwargs.update({
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
        kwargs['first_release'] = release
    try:
        (group, is_new, is_regression, is_sample) = self._save_aggregate(event=event, hashes=hashes, release=release, **kwargs)
    except HashDiscarded:
        event_discarded.send_robust(project=project, sender=EventManager)
        metrics.incr('events.discarded', skip_internal=True, tags={
            'organization_id': project.organization_id,
            'platform': platform,
        })
        raise
    else:
        event_saved.send_robust(project=project, event_size=event.size, sender=EventManager)
    event.group = group
    event.data.bind_ref(event)
    if is_sample:
        try:
            with transaction.atomic(using=router.db_for_write(EventMapping)):
                EventMapping.objects.create(project=project, group=group, event_id=event_id)
        except IntegrityError:
            logger.info('duplicate.found', exc_info=True, extra={
                'event_uuid': event_id,
                'project_id': project.id,
                'group_id': group.id,
                'model': EventMapping.__name__,
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
            logger.info('duplicate.found', exc_info=True, extra={
                'event_uuid': event_id,
                'project_id': project.id,
                'group_id': group.id,
                'model': Event.__name__,
            })
            return event
        index_event_tags.delay(organization_id=project.organization_id, project_id=project.id, group_id=group.id, environment_id=environment.id, event_id=event.id, tags=tags, date_added=event.datetime)
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
            first_event_received.send_robust(project=project, group=group, sender=Project)
    eventstream.insert(group=group, event=event, is_new=is_new, is_sample=is_sample, is_regression=is_regression, is_new_group_environment=is_new_group_environment, primary_hash=hashes[0], skip_consume=raw)
    metrics.timing('events.latency', (received_timestamp - recorded_timestamp), tags={
        'project_id': project.id,
    })
    return event