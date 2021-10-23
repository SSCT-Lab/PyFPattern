def chunk(self):
    conditions = []
    if (self.last_event is not None):
        conditions.extend([['timestamp', '<=', self.last_event.timestamp], [['timestamp', '<', self.last_event.timestamp], ['event_id', '<', self.last_event.event_id]]])
    events = eventstore.get_events(filter=eventstore.Filter(conditions=conditions, project_ids=[self.project_id], group_ids=[self.group_id]), limit=self.DEFAULT_CHUNK_SIZE, referrer='deletions.group', orderby=['-timestamp', '-event_id'])
    if (not events):
        return False
    self.last_event = events[(- 1)]
    node_ids = [Event.generate_node_id(self.project_id, event.event_id) for event in events]
    nodestore.delete_multi(node_ids)
    event_ids = [event.event_id for event in events]
    EventAttachment.objects.filter(event_id__in=event_ids, project_id=self.project_id).delete()
    UserReport.objects.filter(event_id__in=event_ids, project_id=self.project_id).delete()
    return True