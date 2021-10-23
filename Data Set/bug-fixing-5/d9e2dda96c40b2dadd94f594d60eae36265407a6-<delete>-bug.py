def delete(self, request, project, team_slug):
    "\n        Revoke a team's access to a project\n        ```````````````````````````````````\n        :pparam string organization_slug: the slug of the organization.\n        :pparam string project_slug: the slug of the project.\n        :pparam string team_slug: the slug of the project.\n        :auth: required\n        "
    try:
        team = Team.objects.get(organization_id=project.organization_id, slug=team_slug)
    except Team.DoesNotExist:
        raise Http404
    if (not request.access.has_team_scope(team, 'project:write')):
        return Response({
            'detail': ['You do not have permission to perform this action.'],
        }, status=403)
    project.remove_team(team)
    return Response(serialize(project, request.user, ProjectWithTeamSerializer()), status=200)