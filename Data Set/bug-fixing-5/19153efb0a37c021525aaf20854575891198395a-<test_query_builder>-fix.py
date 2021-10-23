def test_query_builder(self):
    with self.feature('organizations:discover'):
        self.browser.get(self.path)
        self.browser.wait_until_not('.loading')
        self.browser.wait_until_not('.is-disabled')
        self.browser.snapshot('discover - query builder')