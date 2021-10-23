def test_javascript_specific_event(self):
    event = self.create_sample_event(platform='javascript')
    self.browser.get('/{}/{}/issues/{}/events/{}/'.format(self.org.slug, self.project.slug, event.group.id, event.id))
    self.browser.wait_until('.event-details-container')
    self.browser.wait_until_not('.loading-indicator')
    self.browser.snapshot('issue details javascript - event details')