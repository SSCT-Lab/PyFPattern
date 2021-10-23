def test_one_issue(self):
    self.project.update(first_event=timezone.now())
    self.browser.get(self.path)
    self.browser.wait_until('.organization-home')
    self.browser.wait_until('.dashboard-barchart')
    self.browser.wait_until_not('.loading-indicator')
    assert (not self.browser.element_exists('.awaiting-events'))
    self.browser.snapshot('org dash one issue')