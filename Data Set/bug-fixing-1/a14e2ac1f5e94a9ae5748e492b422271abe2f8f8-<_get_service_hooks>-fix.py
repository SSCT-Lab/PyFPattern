

def _get_service_hooks(project_id):
    from sentry.models import ServiceHook
    cache_key = 'servicehooks:1:{}'.format(project_id)
    result = cache.get(cache_key)
    if (result is None):
        result = [(h.id, h.events) for h in ServiceHook.objects.filter(project_id=project_id)]
        cache.set(cache_key, result, 60)
    return result
