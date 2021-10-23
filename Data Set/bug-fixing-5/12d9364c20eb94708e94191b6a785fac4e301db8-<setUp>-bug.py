def setUp(self):
    super(IssueDetailsTest, self).setUp()
    self.user = self.create_user('foo@example.com')
    self.org = self.create_organization(owner=self.user, name='Rowdy Tiger')
    self.team = self.create_team(organization=self.org, name='Mariachi Band')
    self.project = self.create_project(organization=self.org, teams=[self.team], name='Bengal')
    self.login_as(self.user)