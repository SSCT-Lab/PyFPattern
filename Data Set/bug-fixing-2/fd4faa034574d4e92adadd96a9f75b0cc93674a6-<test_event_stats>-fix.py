

def test_event_stats(self):
    now = datetime.now()
    with freeze_time((now - timedelta(days=1)).replace(hour=12, minute=30, second=25)):
        for _ in range(2):
            self.store_event(data={
                'event_id': uuid4().hex,
                'fingerprint': ['group1'],
                'timestamp': iso_format(before_now(seconds=1)),
            }, project_id=self.project.id)
        incident = self.create_incident(date_started=(timezone.now() - timedelta(hours=2)), projects=[self.project], query='')
        snapshot = create_initial_event_stats_snapshot(incident)
        activity = create_incident_activity(incident=incident, activity_type=IncidentActivityType.COMMENT, user=self.user, comment='hello', event_stats_snapshot=snapshot)
        result = serialize(activity)
        assert (result['id'] == six.text_type(activity.id))
        assert (result['incidentIdentifier'] == six.text_type(activity.incident.identifier))
        assert (result['user'] == serialize(activity.user))
        assert (result['type'] == activity.type)
        assert (result['value'] is None)
        assert (result['previousValue'] is None)
        assert (result['comment'] == activity.comment)
        event_stats = result['eventStats']['data']
        assert ([stat[1] for stat in event_stats[:(- 1)]] == ([[]] * len(event_stats[:(- 1)])))
        assert (event_stats[(- 1)][1] == [{
            'count': 2,
        }])
        assert (result['dateCreated'] == activity.date_added)
