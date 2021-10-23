def setUp(self):
    super(OrganizationOnboardingTest, self).setUp()
    self.user = self.create_user('foo@example.com')
    self.org = self.create_organization(name='Rowdy Tiger', owner=self.user)
    self.team = self.create_team(organization=self.org, name='Mariachi Band')
    self.member = self.create_member(user=None, email='bar@example.com', organization=self.org, role='owner', teams=[self.team])
    self.login_as(self.user)