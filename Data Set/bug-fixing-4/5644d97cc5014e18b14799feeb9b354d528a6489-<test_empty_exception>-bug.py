def test_empty_exception(self):
    event = self.create_sample_event(platform='empty-exception')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.browser.wait_until('.entries')
    self.browser.snapshot('issue details empty exception')