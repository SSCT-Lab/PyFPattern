@instrumented_task(name='sentry.tasks.post_process.post_process_group')
def post_process_group(event, is_new, is_regression, is_sample, is_new_group_environment, **kwargs):
    '\n    Fires post processing hooks for a group.\n    '
    with snuba.options_override({
        'consistent': True,
    }):
        if check_event_already_post_processed(event):
            logger.info('post_process.skipped', extra={
                'project_id': event.project_id,
                'event_id': event.event_id,
                'reason': 'duplicate',
            })
            return
        from sentry.models import Project
        from sentry.models.group import get_group_with_redirect
        from sentry.rules.processor import RuleProcessor
        from sentry.tasks.servicehooks import process_service_hook
        (event.group, _) = get_group_with_redirect(event.group_id)
        event.group_id = event.group.id
        project_id = event.group.project_id
        with configure_scope() as scope:
            scope.set_tag('project', project_id)
        event.project = Project.objects.get_from_cache(id=project_id)
        _capture_stats(event, is_new)
        has_reappeared = process_snoozes(event.group)
        rp = RuleProcessor(event, is_new, is_regression, is_new_group_environment, has_reappeared)
        has_alert = False
        for (callback, futures) in rp.apply():
            has_alert = True
            safe_execute(callback, event, futures)
        if features.has('projects:servicehooks', project=event.project):
            allowed_events = set(['event.created'])
            if has_alert:
                allowed_events.add('event.alert')
            if allowed_events:
                for (servicehook_id, events) in _get_service_hooks(project_id=event.project_id):
                    if any(((e in allowed_events) for e in events)):
                        process_service_hook.delay(servicehook_id=servicehook_id, event=event)
        for plugin in plugins.for_project(event.project):
            plugin_post_process_group(plugin_slug=plugin.slug, event=event, is_new=is_new, is_regresion=is_regression, is_sample=is_sample)
        event_processed.send_robust(sender=post_process_group, project=event.project, group=event.group, event=event, primary_hash=kwargs.get('primary_hash'))