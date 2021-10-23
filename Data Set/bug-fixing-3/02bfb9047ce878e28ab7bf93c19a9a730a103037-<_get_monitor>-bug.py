def _get_monitor(module):
    if (module.params['id'] is not None):
        monitor = api.Monitor.get(module.params['id'])
        if ('errors' in monitor):
            module.fail_json(msg=('Failed to retrieve monitor with id %s, errors are %s' % (module.params['id'], str(monitor['errors']))))
        return monitor
    else:
        monitors = api.Monitor.get_all()
        for monitor in monitors:
            if (monitor['name'] == module.params['name']):
                return monitor
    return {
        
    }