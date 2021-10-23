def handle_state(module, result, service_path):
    "Set service running state as needed.\n\n    Takes into account the fact that a service may not be loaded (no supervise directory) in\n    which case it is 'stopped' as far as the service manager is concerned. No status information\n    can be obtained and the service can only be 'started'.\n    "
    result['state'] = module.params['state']
    action = None
    if (module.check_mode and ((module.params['enabled'] is not None) or module.params['preset'])):
        enabled = result['enabled']
    else:
        enabled = service_is_enabled(module, service_path)
    if (not service_is_loaded(module, service_path)):
        if (module.params['state'] in ['started', 'restarted', 'reloaded']):
            action = 'start'
            result['state'] = 'started'
        elif (module.params['state'] == 'reset'):
            if enabled:
                action = 'start'
                result['state'] = 'started'
            else:
                result['state'] = 'stopped'
        else:
            result['state'] = 'stopped'
    else:
        result['status'] = get_service_status(module, service_path)
        running = service_is_running(result['status'])
        if (module.params['state'] == 'started'):
            if (not running):
                action = 'start'
        elif (module.params['state'] == 'stopped'):
            if running:
                action = 'stop'
        elif (module.params['state'] == 'reset'):
            if (enabled is not running):
                if running:
                    action = 'stop'
                    result['state'] = 'stopped'
                else:
                    action = 'start'
                    result['state'] = 'started'
        elif (module.params['state'] == 'restarted'):
            if (not running):
                action = 'start'
                result['state'] = 'started'
            else:
                action = 'condrestart'
        elif (module.params['state'] == 'reloaded'):
            if (not running):
                action = 'start'
                result['state'] = 'started'
            else:
                action = 'hangup'
    if action:
        result['changed'] = True
        if (not module.check_mode):
            (rc, out, err) = run_sys_ctl(module, [action, service_path])
            if (rc != 0):
                module.fail_json(msg=('Unable to %s service %s: %s' % (action, service_path, err)))