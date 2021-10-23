def test_invalid_interfaces(self):
    event = self.create_sample_event(platform='invalid-interfaces')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.wait_until_loaded(skip_assistant=True)
    self.browser.click('.errors-toggle')
    self.browser.wait_until('.entries > .errors ul')
    self.browser.snapshot('issue details invalid interfaces')