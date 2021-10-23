def _get_default_project_id(cloud, default_project, domain_id, module):
    project = cloud.get_project(default_project, domain_id=domain_id)
    if (not project):
        module.fail_json(msg=('Default project %s is not valid' % default_project))
    return project['id']