def test_with_no_releases(self):
    self.browser.get(self.path)
    self.browser.wait_until_not('.loading')
    self.browser.wait_until('.ref-project-releases')
    self.browser.snapshot('project releases without releases')