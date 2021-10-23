@mock.patch('sentry.models.ProjectKey.generate_api_key', return_value='test-dsn')
def test_onboarding(self, generate_api_key):
    self.browser.get(('/onboarding/%s/' % self.org.slug))
    self.browser.wait_until('[data-test-id="onboarding-step-welcome"]')
    self.browser.snapshot(name='onboarding - welcome')
    self.browser.click('[data-test-id="welcome-next"]')
    self.browser.wait_until('[data-test-id="onboarding-step-select-platform"]')
    self.browser.snapshot(name='onboarding - select platform')
    self.browser.click('[data-test-id="platform-node"]')
    self.browser.wait_until_not('[data-test-id="platform-select-next"][aria-disabled="true"]')
    self.browser.click('[data-test-id="platform-select-next"]')
    self.browser.wait_until('[data-test-id="onboarding-step-get-started"]')
    self.browser.snapshot(name='onboarding - get started')
    project = Project.objects.get(organization=self.org)
    assert (project.name == 'rowdy-tiger')
    assert (project.platform == 'node')
    self.browser.click('[data-test-id="onboarding-getting-started-invite-members"]')
    self.browser.snapshot(name='onboarding - invite members')
    self.browser.click('[data-test-id="onboarding-getting-started-learn-more"]')
    self.browser.snapshot(name='onboarding - learn more')