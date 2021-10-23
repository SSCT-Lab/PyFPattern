

def insert(self, group, event, is_new, is_sample, is_regression, is_new_group_environment, primary_hash, skip_consume=False):
    if options.get('eventstream.kafka.send-post_process-task'):
        super(KafkaEventStream, self).insert(group, event, is_new, is_sample, is_regression, is_new_group_environment, primary_hash, skip_consume)
    project = event.project
    retention_days = quotas.get_event_retention(organization=Organization(project.organization_id))
    self._send(project.id, 'insert', extra_data=({
        'group_id': event.group_id,
        'event_id': event.event_id,
        'organization_id': project.organization_id,
        'project_id': event.project_id,
        'message': event.real_message,
        'platform': event.platform,
        'datetime': event.datetime,
        'data': dict(event.data.items()),
        'primary_hash': primary_hash,
        'retention_days': retention_days,
    }, {
        'is_new': is_new,
        'is_sample': is_sample,
        'is_regression': is_regression,
        'is_new_group_environment': is_new_group_environment,
    }))
