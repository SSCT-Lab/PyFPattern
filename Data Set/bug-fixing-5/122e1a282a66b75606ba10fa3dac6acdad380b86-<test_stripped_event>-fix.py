def test_stripped_event(self):
    event = self.create_sample_event(platform='pii')
    self.visit_issue(event.group.id)
    self.browser.snapshot('issue details pii stripped')