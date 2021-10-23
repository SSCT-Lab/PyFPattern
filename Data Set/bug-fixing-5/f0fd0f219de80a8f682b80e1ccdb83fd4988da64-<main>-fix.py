def main():
    module = AnsibleModule(argument_spec=dict(state=dict(required=True, choices=['started', 'paused']), apikey=dict(required=True, no_log=True), monitorid=dict(required=True)), supports_check_mode=SUPPORTS_CHECK_MODE)
    params = dict(apiKey=module.params['apikey'], monitors=module.params['monitorid'], monitorID=module.params['monitorid'], format=API_FORMAT, noJsonCallback=API_NOJSONCALLBACK)
    check_result = checkID(module, params)
    if (check_result['stat'] != 'ok'):
        module.fail_json(msg='failed', result=check_result['message'])
    if (module.params['state'] == 'started'):
        monitor_result = startMonitor(module, params)
    else:
        monitor_result = pauseMonitor(module, params)
    module.exit_json(msg='success', result=monitor_result)