@patch('django.utils.timezone.now')
def test_modal_from_all_events(self, mock_now):
    mock_now.return_value = datetime.utcnow().replace(tzinfo=pytz.utc)
    min_ago = (timezone.now() - timedelta(minutes=1)).isoformat()[:19]
    event_data = load_data('python')
    event_data['timestamp'] = min_ago
    event_data['received'] = min_ago
    event_data['fingerprint'] = ['group-1']
    self.store_event(data=event_data, project_id=self.project.id, assert_no_errors=False)
    with self.feature(FEATURE_NAME):
        self.browser.get(self.path)
        self.wait_until_loaded()
        self.browser.element('[data-test-id="event-title"]').click()
        self.wait_until_loaded()
        header = self.browser.element('[data-test-id="modal-dialog"] h2')
        assert (event_data['message'] in header.text)
        self.browser.snapshot('events-v2 - single error modal')