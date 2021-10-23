def test_cocoa_event(self):
    event = self.create_sample_event(platform='cocoa')
    self.visit_issue(event.group.id)
    self.browser.snapshot('issue details cocoa')