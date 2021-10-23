def test_empty_stacktrace(self):
    event = self.create_sample_event(platform='empty-stacktrace')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.wait_until_loaded(skip_assistant=True)
    self.browser.snapshot('issue details empty stacktrace')