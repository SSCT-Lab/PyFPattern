def setUp(self):
    self.user = self.create_user('coreapi@example.com')
    self.team = self.create_team(name='Foo')
    self.project = self.create_project(team=self.team)
    self.pk = self.project.key_set.get_or_create()[0]
    self.helper = self.helper_cls(agent='Awesome Browser', ip_address='198.51.100.0')