def test_empty_stacktrace(self):
    event = self.create_sample_event(platform='empty-stacktrace')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.browser.wait_until('.entries')
    self.browser.wait_until('[data-test-id="linked-issues"]')
    self.browser.snapshot('issue details empty stacktrace')