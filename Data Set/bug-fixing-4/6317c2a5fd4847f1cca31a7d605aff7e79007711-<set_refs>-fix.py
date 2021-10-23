def set_refs(self, release, **values):
    if (not values.get('owner', None)):
        return
    repo_project_option = ProjectOption.objects.get_value(project=self.project, key='heroku:repository')
    deploy_project_option = (ProjectOption.objects.get_value(project=self.project, key='heroku:environment', default='production') or 'production')
    if repo_project_option:
        try:
            repository = Repository.objects.get(organization_id=self.project.organization_id, name=repo_project_option)
        except Repository.DoesNotExist:
            logger.info('repository.missing', extra={
                'organization_id': self.project.organization_id,
                'project_id': self.project.id,
                'repository': repo_project_option,
            })
        else:
            release.set_refs(refs=[{
                'commit': release.version,
                'repository': repository.name,
            }], user=values['owner'], fetch=True)
    endpoint = '/organizations/{}/releases/{}/deploys/'.format(self.project.organization.slug, release.version)
    auth = ApiKey(organization=self.project.organization, scope_list=['project:write'])
    client.post(endpoint, data={
        'environment': deploy_project_option,
    }, auth=auth)