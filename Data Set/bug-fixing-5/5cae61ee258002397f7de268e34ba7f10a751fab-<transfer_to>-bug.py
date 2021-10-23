def transfer_to(self, team):
    from sentry.models import ProjectTeam, ReleaseProject
    organization = team.organization
    from_team_id = self.team_id
    old_org_id = self.organization_id
    org_changed = (old_org_id != organization.id)
    if org_changed:
        ReleaseProject.objects.filter(project_id=self.id).delete()
    self.organization = organization
    self.team = team
    try:
        with transaction.atomic():
            self.update(organization=organization, team=team)
    except IntegrityError:
        slugify_instance(self, self.name, organization=organization)
        self.update(slug=self.slug, organization=organization, team=team)
    ProjectTeam.objects.filter(project=self, team_id=from_team_id).update(team=team)
    if org_changed:
        ProjectTeam.objects.filter(project=self, team__organization_id=old_org_id).delete()
    self.add_team(team)