def merge_to(from_org, to_org):
    from sentry.models import ApiKey, AuditLogEntry, Commit, OrganizationMember, OrganizationMemberTeam, Project, Release, ReleaseCommit, ReleaseEnvironment, ReleaseFile, Repository, Team
    for from_member in OrganizationMember.objects.filter(organization=from_org):
        try:
            to_member = OrganizationMember.objects.get(organization=to_org, user=from_member.user)
        except OrganizationMember.DoesNotExist:
            from_member.update(organization=to_org)
            to_member = from_member
        else:
            qs = OrganizationMemberTeam.objects.filter(organizationmember=from_member, is_active=True).select_related()
            for omt in qs:
                OrganizationMemberTeam.objects.create_or_update(organizationmember=to_member, team=omt.team, defaults={
                    'is_active': True,
                })
    for team in Team.objects.filter(organization=from_org):
        try:
            with transaction.atomic():
                team.update(organization=to_org)
        except IntegrityError:
            slugify_instance(team, team.name, organization=to_org)
            team.update(organization=to_org, slug=team.slug)
    for project in Project.objects.filter(organization=from_org):
        try:
            with transaction.atomic():
                project.update(organization=to_org)
        except IntegrityError:
            slugify_instance(project, project.name, organization=to_org)
            project.update(organization=to_org, slug=project.slug)
    for release in Release.objects.filter(organization=from_org):
        try:
            to_release = Release.objects.get(version=release.version, organization=to_org)
        except Release.DoesNotExist:
            Release.objects.filter(id=release.id).update(organization=to_org)
        else:
            Release.merge(to_release, [release])
    for model in (ApiKey, AuditLogEntry, ReleaseFile):
        model.objects.filter(organization=from_org).update(organization=to_org)
    for model in (Commit, ReleaseCommit, ReleaseEnvironment, Repository):
        model.objects.filter(organization_id=from_org.id).update(organization_id=to_org.id)