def test_cordova_event(self):
    event = self.create_sample_event(platform='cordova')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.wait_until_loaded()
    self.browser.snapshot('issue details cordova')