def get_for_user(self, organization, user, scope=None, with_projects=False):
    '\n        Returns a list of all teams a user has some level of access to.\n        '
    from sentry.auth.superuser import is_active_superuser
    from sentry.models import OrganizationMemberTeam, Project, ProjectStatus, ProjectTeam, OrganizationMember
    if (not user.is_authenticated()):
        return []
    base_team_qs = self.filter(organization=organization, status=TeamStatus.VISIBLE)
    if ((env.request and is_active_superuser(env.request)) or settings.SENTRY_PUBLIC):
        team_list = list(base_team_qs)
    else:
        try:
            om = OrganizationMember.objects.get(user=user, organization=organization)
        except OrganizationMember.DoesNotExist:
            return []
        if ((scope is not None) and (scope not in om.get_scopes())):
            return []
        team_list = list(base_team_qs.filter(id__in=OrganizationMemberTeam.objects.filter(organizationmember=om, is_active=True).values_list('team')))
    results = sorted(team_list, key=(lambda x: x.name.lower()))
    if with_projects:
        project_list = sorted(Project.objects.filter(teams__in=team_list, status=ProjectStatus.VISIBLE), key=(lambda x: x.name.lower()))
        teams_by_project = defaultdict(set)
        for (project_id, team_id) in ProjectTeam.objects.filter(project__in=project_list).values_list('project_id', 'team_id'):
            teams_by_project[project_id].add(team_id)
        projects_by_team = {t.id: [] for t in team_list}
        for project in project_list:
            for team_id in teams_by_project[project.id]:
                projects_by_team[team_id].append(project)
        for (idx, team) in enumerate(results):
            team_projects = projects_by_team[team.id]
            results[idx] = (team, team_projects)
    return results