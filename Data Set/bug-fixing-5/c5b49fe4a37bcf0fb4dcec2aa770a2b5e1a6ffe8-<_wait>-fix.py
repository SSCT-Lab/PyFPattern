def _wait(timeout, cloud, server, action, module, sdk):
    'Wait for the server to reach the desired state for the given action.'
    for count in sdk.utils.iterate_timeout(timeout, ('Timeout waiting for server to complete %s' % action)):
        try:
            server = cloud.get_server(server.id)
        except Exception:
            continue
        if (server.status == _action_map[action]):
            return
        if (server.status == 'ERROR'):
            module.fail_json(msg=('Server reached ERROR state while attempting to %s' % action))