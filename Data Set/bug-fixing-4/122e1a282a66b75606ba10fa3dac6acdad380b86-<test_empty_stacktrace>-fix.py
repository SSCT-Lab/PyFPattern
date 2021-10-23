def test_empty_stacktrace(self):
    event = self.create_sample_event(platform='empty-stacktrace')
    self.visit_issue(event.group.id)
    self.browser.snapshot('issue details empty stacktrace')