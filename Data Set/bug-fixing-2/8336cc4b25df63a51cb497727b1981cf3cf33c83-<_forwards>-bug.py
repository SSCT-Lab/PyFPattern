

def _forwards(self, orm):
    'Write your forwards methods here.'
    from sentry.utils.query import RangeQuerySetWrapperWithProgressBar
    ServiceHook = orm['sentry.ServiceHook']
    ServiceHookProject = orm['sentry.ServiceHookProject']
    Project = orm['sentry.Project']
    queryset = ServiceHook.objects.all()
    for service_hook in RangeQuerySetWrapperWithProgressBar(queryset):
        try:
            with transaction.atomic():
                ServiceHookProject.objects.create(project_id=service_hook.project_id, service_hook_id=service_hook.id)
                project = Project.objects.get(id=service_hook.project_id)
                service_hook.update(organization_id=project.organization_id)
        except IntegrityError:
            pass
