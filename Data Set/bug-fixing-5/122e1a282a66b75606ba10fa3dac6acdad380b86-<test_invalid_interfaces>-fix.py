def test_invalid_interfaces(self):
    event = self.create_sample_event(platform='invalid-interfaces')
    self.visit_issue(event.group.id)
    self.browser.click('.errors-toggle')
    self.browser.wait_until('.entries > .errors ul')
    self.browser.snapshot('issue details invalid interfaces')