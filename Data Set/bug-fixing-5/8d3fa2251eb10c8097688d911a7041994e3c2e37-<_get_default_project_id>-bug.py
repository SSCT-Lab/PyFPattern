def _get_default_project_id(cloud, default_project, module):
    project = cloud.get_project(default_project)
    if (not project):
        module.fail_json(msg=('Default project %s is not valid' % default_project))
    return project['id']