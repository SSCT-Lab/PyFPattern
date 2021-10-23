def test_run_query(self):
    with self.feature('organizations:discover'):
        self.browser.get(self.path)
        self.browser.wait_until_not('.loading')
        self.browser.find_element_by_xpath("//button//span[contains(text(), 'Run')]").click()
        self.browser.wait_until_not('.loading')
        self.browser.snapshot('discover - query results')