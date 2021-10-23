@patch('django.utils.timezone.now')
def test_run_query(self, mock_now):
    mock_now.return_value = before_now().replace(tzinfo=pytz.utc)
    with self.feature('organizations:discover'):
        self.browser.get(self.path)
        self.browser.wait_until_not('.loading')
        self.browser.find_element_by_xpath("//button//span[contains(text(), 'Run')]").click()
        self.browser.wait_until_not('.loading')
        self.browser.snapshot('discover - query results')
        self.browser.save_screenshot('discover1.png')