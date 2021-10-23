def test_no_issues(self):
    self.project.update(first_event=None)
    self.browser.get(self.path)
    self.browser.wait_until('.organization-home')
    self.browser.wait_until('.dashboard-barchart')
    self.browser.wait_until('.awaiting-events')
    self.browser.wait_until_not('.loading-indicator')
    self.browser.snapshot('org dash no issues')