def test_python_event(self):
    event = self.create_sample_event(platform='python')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.browser.wait_until('.entries')
    self.browser.snapshot('issue details python')