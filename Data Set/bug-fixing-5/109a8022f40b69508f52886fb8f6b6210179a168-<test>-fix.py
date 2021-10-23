def test(self):
    with self.feature('organizations:sentry10'):
        self.create_group(project=self.project, message='Foo bar')
        self.create_userreport(group=self.group, project=self.project, event=self.event)
        self.browser.get(self.path)
        self.browser.wait_until_not('.loading-indicator')
        self.browser.snapshot('organization user feedback')