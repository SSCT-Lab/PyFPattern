def test_unity_event(self):
    event = self.create_sample_event(default='unity', platform='csharp')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.wait_until_loaded()
    self.browser.snapshot('issue details unity')