@suppress_errors
def report_monitor_begin(task, **kwargs):
    monitor_id = task.request.headers.get('X-Sentry-Monitor')
    with configure_scope() as scope:
        if monitor_id:
            scope.set_context('monitor', {
                'id': monitor_id,
            })
        else:
            scope.remove_context('monitor')
    if ((not SENTRY_DSN) or (not API_ROOT)):
        return
    if (not monitor_id):
        return
    session = SafeSession()
    req = session.post('{}/api/0/monitors/{}/checkins/'.format(API_ROOT, monitor_id), headers={
        'Authorization': 'DSN {}'.format(SENTRY_DSN),
    }, json={
        'status': 'in_progress',
    })
    req.raise_for_status()
    task.request.headers['X-Sentry-Monitor-CheckIn'] = (req.json()['id'], time())