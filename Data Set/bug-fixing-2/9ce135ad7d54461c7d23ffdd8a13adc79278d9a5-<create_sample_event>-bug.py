

def create_sample_event(self, platform, default=None, sample_name=None, time=None):
    event_data = load_data(platform, default=default, sample_name=sample_name)
    event_data['event_id'] = 'd964fdbd649a4cf8bfc35d18082b6b0e'
    if time:
        event_data['received'] = time.isoformat()
    if (time is None):
        time = (now - timedelta(days=1))
    event_data['timestamp'] = time.isoformat()
    event = self.store_event(data=event_data, project_id=self.project.id, assert_no_errors=False)
    event.group.update(first_seen=datetime(2015, 8, 13, 3, 8, 25, tzinfo=timezone.utc), last_seen=time)
    return event
