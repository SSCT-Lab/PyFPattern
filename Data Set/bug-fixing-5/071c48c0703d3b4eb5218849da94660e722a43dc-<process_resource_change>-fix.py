@instrumented_task('sentry.tasks.process_resource_change', default_retry_delay=(60 * 5), max_retries=5)
@retry()
def process_resource_change(sender, instance_id, created):
    model = sender.__name__
    model = RESOURCE_RENAMES.get(model, model.lower())
    instance = sender.objects.get(id=instance_id)
    event = ('created' if created else 'updated')
    action = '{}.{}'.format(model, event)
    if (action not in ALLOWED_ACTIONS):
        return
    project = None
    if isinstance(instance, Group):
        project = instance.project
    if (not project):
        return
    servicehooks = ServiceHook.objects.filter(project_id=project.id)
    for servicehook in filter((lambda s: (action in s.events)), servicehooks):
        if (not servicehook.created_by_sentry_app):
            continue
        payload = app_platform_event(action, SentryAppInstallation.objects.get(id=servicehook.actor_id), serialize(instance))
        send_request(servicehook, payload, verify_ssl=True)