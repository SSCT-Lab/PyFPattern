@patch('django.utils.timezone.now')
def test_all_events(self, mock_now):
    mock_now.return_value = datetime.utcnow().replace(tzinfo=pytz.utc)
    min_ago = (timezone.now() - timedelta(minutes=1)).isoformat()[:19]
    self.store_event(data={
        'event_id': ('a' * 32),
        'message': 'oh no',
        'timestamp': min_ago,
        'fingerprint': ['group-1'],
    }, project_id=self.project.id, assert_no_errors=False)
    with self.feature(FEATURE_NAME):
        self.browser.get(self.path)
        self.browser.wait_until_not('.loading-indicator')
        self.browser.snapshot('events-v2 - all events')