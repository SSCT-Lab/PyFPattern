@instrumented_task(name='sentry.tasks.process_service_hook', default_retry_delay=(60 * 5), max_retries=5)
def process_service_hook(servicehook_id, event, **kwargs):
    from sentry import tsdb
    from sentry.models import ServiceHook
    try:
        servicehook = ServiceHook.objects.get(id=servicehook_id)
    except ServiceHook.DoesNotExist:
        return
    tsdb.incr(tsdb.models.servicehook_fired, servicehook.id)
    if (servicehook.version == 0):
        payload = get_payload_v0(event)
    else:
        raise NotImplementedError
    body = json.dumps(payload)
    headers = {
        'Content-Type': 'application/json',
        'X-ServiceHook-Timestamp': int(time()),
        'X-ServiceHook-GUID': servicehook.guid,
        'X-ServiceHook-Signature': servicehook.build_signature(body),
    }
    safe_urlopen(url=servicehook.url, data=body, headers=headers, timeout=5, verify_ssl=False)