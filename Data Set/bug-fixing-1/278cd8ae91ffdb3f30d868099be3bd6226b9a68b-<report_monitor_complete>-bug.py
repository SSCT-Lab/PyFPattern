

@suppress_errors
def report_monitor_complete(task, retval, **kwargs):
    if ((not SENTRY_DSN) or (not API_ROOT)):
        return
    monitor_id = task.request.headers.get('X-Sentry-Monitor')
    if (not monitor_id):
        return
    try:
        (checkin_id, start_time) = task.request.headers.get('X-Sentry-Monitor-CheckIn')
    except (ValueError, TypeError):
        return
    duration = int((time() - (start_time * 1000)))
    session = SafeSession()
    session.put('{}/api/0/monitors/{}/checkins/{}/'.format(API_ROOT, monitor_id, checkin_id), headers={
        'Authorization': 'DSN {}'.format(SENTRY_DSN),
    }, json={
        'status': ('error' if isinstance(retval, Exception) else 'ok'),
        'duration': duration,
    }).raise_for_status()
