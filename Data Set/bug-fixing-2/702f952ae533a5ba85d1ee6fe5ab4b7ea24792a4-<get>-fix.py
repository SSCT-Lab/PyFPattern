

def get(self, request, project):
    try:
        environment_id = self._get_environment_id_from_request(request, project.organization_id)
    except Environment.DoesNotExist:
        raise ResourceDoesNotExist
    now = timezone.now()
    then = (now - timedelta(days=30))
    results = tsdb.get_distinct_counts_series(tsdb.models.users_affected_by_project, (project.id,), then, now, rollup=(3600 * 24), environment_id=environment_id)[project.id]
    return Response(results)
