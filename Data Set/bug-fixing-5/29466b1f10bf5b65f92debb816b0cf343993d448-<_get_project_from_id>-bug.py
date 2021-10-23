def _get_project_from_id(self, project_id):
    if (not project_id):
        return
    if (not project_id.isdigit()):
        track_outcome(0, 0, None, Outcome.INVALID, 'project_id')
        raise APIError(('Invalid project_id: %r' % project_id))
    try:
        return Project.objects.get_from_cache(id=project_id)
    except Project.DoesNotExist:
        track_outcome(0, 0, None, Outcome.INVALID, 'project_id')
        raise APIError(('Invalid project_id: %r' % project_id))