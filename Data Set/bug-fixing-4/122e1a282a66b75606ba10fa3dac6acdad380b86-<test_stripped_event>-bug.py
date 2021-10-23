def test_stripped_event(self):
    event = self.create_sample_event(platform='pii')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.wait_until_loaded()
    self.browser.snapshot('issue details pii stripped')