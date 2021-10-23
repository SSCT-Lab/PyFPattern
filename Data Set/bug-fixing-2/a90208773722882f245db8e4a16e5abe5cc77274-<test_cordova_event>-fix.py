

def test_cordova_event(self):
    event = self.create_sample_event(platform='cordova')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.browser.wait_until('.entries')
    self.browser.wait_until('[data-test-id="loaded-device-name"]')
    self.browser.snapshot('issue details cordova')
