def test_aspnetcore_event(self):
    event = self.create_sample_event(default='aspnetcore', platform='csharp')
    self.visit_issue(event.group.id)
    self.browser.snapshot('issue details aspnetcore')