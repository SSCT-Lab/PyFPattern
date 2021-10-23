def test_invalid_interfaces(self):
    event = self.create_sample_event(platform='invalid-interfaces')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.wait_until_loaded()
    self.browser.snapshot('issue details invalid interfaces')