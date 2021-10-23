def forwards(self, orm):
    'Write your forwards methods here.'
    for (project_id, organization_id) in WithProgressBar(orm.Project.objects.all().values_list('id', 'organization_id')):
        orm.ReleaseEnvironment.objects.filter(project_id=project_id, organization_id__isnull=True).update(organization_id=organization_id)
        orm.ReleaseFile.objects.filter(project_id=project_id, organization_id__isnull=True).update(organization=organization_id)