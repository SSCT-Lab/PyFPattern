def insert(self, group, event, is_new, is_sample, is_regression, is_new_group_environment, primary_hash, skip_consume=False):
    project = event.project
    retention_days = quotas.get_event_retention(organization=project.organization)
    event_data = event.get_raw_data()
    unexpected_tags = set([k for (k, v) in (get_path(event_data, 'tags') or []) if (k in self.UNEXPECTED_TAG_KEYS)])
    if unexpected_tags:
        logger.error('%r received unexpected tags: %r', self, unexpected_tags)
    self._send(project.id, 'insert', extra_data=({
        'group_id': event.group_id,
        'event_id': event.event_id,
        'organization_id': project.organization_id,
        'project_id': event.project_id,
        'message': event.message,
        'platform': event.platform,
        'datetime': event.datetime,
        'data': event_data,
        'primary_hash': primary_hash,
        'retention_days': retention_days,
    }, {
        'is_new': is_new,
        'is_sample': is_sample,
        'is_regression': is_regression,
        'is_new_group_environment': is_new_group_environment,
        'skip_consume': skip_consume,
    }))