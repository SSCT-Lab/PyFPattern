

def test_simple(self):
    self.team = self.create_team(organization=self.org, name='Mariachi Band')
    self.create_member(user=self.user, organization=self.org, role='owner', teams=[self.team])
    self.browser.get(self.path)
    self.browser.wait_until_not('.loading')
    self.browser.click('.platformicon-java')
    self.browser.snapshot(name='create project')
    self.browser.click('.new-project-submit')
    self.browser.wait_until(title='Java')
    project = Project.objects.get(organization=self.org)
    assert (project.name == 'Java')
    assert (project.platform == 'java')
    assert (project.team_id == self.team.id)
    self.browser.snapshot(name='docs redirect')
