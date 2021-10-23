def send_request(servicehook, payload):
    from sentry import tsdb
    tsdb.incr(tsdb.models.servicehook_fired, servicehook.id)
    headers = {
        'Content-Type': 'application/json',
        'X-ServiceHook-Timestamp': six.text_type(int(time())),
        'X-ServiceHook-GUID': servicehook.guid,
        'X-ServiceHook-Signature': servicehook.build_signature(json.dumps(payload)),
    }
    safe_urlopen(url=servicehook.url, data=json.dumps(payload), headers=headers, timeout=5, verify_ssl=True)