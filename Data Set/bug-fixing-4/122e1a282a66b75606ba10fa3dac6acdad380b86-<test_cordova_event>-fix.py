def test_cordova_event(self):
    event = self.create_sample_event(platform='cordova')
    self.visit_issue(event.group.id)
    self.browser.snapshot('issue details cordova')