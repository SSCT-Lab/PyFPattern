

def get_reprocessing_revision(project, cached=True):
    'Returns the current revision of the projects reprocessing config set.'
    from sentry.models import ProjectOption, Project
    if cached:
        return ProjectOption.objects.get_value(project, REPROCESSING_OPTION)
    try:
        if isinstance(project, Project):
            project = project.id
        return ProjectOption.objects.get(project=project, key=REPROCESSING_OPTION).value
    except ProjectOption.DoesNotExist:
        pass
