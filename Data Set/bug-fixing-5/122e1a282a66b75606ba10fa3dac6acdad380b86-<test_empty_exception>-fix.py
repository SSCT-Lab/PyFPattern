def test_empty_exception(self):
    event = self.create_sample_event(platform='empty-exception')
    self.visit_issue(event.group.id)
    self.browser.snapshot('issue details empty exception')