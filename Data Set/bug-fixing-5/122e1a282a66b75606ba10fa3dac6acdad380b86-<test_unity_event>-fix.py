def test_unity_event(self):
    event = self.create_sample_event(default='unity', platform='csharp')
    self.visit_issue(event.group.id)
    self.browser.snapshot('issue details unity')