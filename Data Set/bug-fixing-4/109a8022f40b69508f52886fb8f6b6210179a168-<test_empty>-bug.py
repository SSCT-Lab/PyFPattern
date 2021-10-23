def test_empty(self):
    with self.feature('organizations:sentry10'):
        self.browser.get(self.path)
        self.browser.snapshot('organization user feedback - empty')