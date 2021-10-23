def test_rust_event(self):
    event = self.create_sample_event(platform='native', sample_name='Rust')
    self.visit_issue(event.group.id)
    self.wait_until_loaded()
    self.browser.snapshot('issue details rust')