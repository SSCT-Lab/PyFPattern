def test_python_event(self):
    event = self.create_sample_event(platform='python')
    self.visit_issue(event.group.id)
    self.browser.snapshot('issue details python')