def test_rust_event(self):
    event = self.create_sample_event(platform='native', sample_name='Rust')
    self.browser.get('/{}/{}/issues/{}/'.format(self.org.slug, self.project.slug, event.group.id))
    self.browser.wait_until('.entries')
    self.browser.snapshot('issue details rust')