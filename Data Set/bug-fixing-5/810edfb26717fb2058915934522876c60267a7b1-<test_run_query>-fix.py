@patch('django.utils.timezone.now')
def test_run_query(self, mock_now):
    mock_now.return_value = before_now().replace(tzinfo=pytz.utc)
    with self.feature('organizations:discover'):
        self.browser.get(self.path)
        self.browser.wait_until_not('.loading')
        self.browser.click_when_visible('[aria-label="Run"]')
        self.browser.wait_until_not('.loading')
        self.browser.wait_until_test_id('result')
        self.browser.snapshot('discover - query results')