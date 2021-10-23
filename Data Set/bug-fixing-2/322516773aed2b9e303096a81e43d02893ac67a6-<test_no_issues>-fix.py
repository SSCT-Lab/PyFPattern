

def test_no_issues(self):
    self.project.update(first_event=None)
    self.browser.get(self.path)
    self.browser.wait_until_not('.loading-indicator')
    self.browser.wait_until('[data-test-id] figure')
    self.browser.snapshot('org dash no issues')
