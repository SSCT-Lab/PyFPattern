def main():
    module = AnsibleModule(argument_spec=dict(api_key=dict(required=True, no_log=True), app_key=dict(required=True, no_log=True), state=dict(required=True, choises=['present', 'absent', 'mute', 'unmute']), type=dict(required=False, choises=['metric alert', 'service check', 'event alert']), name=dict(required=True), query=dict(required=False), message=dict(required=False, default=None), silenced=dict(required=False, default=None, type='dict'), notify_no_data=dict(required=False, default=False, type='bool'), no_data_timeframe=dict(required=False, default=None), timeout_h=dict(required=False, default=None), renotify_interval=dict(required=False, default=None), escalation_message=dict(required=False, default=None), notify_audit=dict(required=False, default=False, type='bool'), thresholds=dict(required=False, type='dict', default=None), tags=dict(required=False, type='list', default=None), locked=dict(required=False, default=False, type='bool'), require_full_window=dict(required=False, default=None, type='bool'), id=dict(required=False)))
    if (not HAS_DATADOG):
        module.fail_json(msg='datadogpy required for this module')
    options = {
        'api_key': module.params['api_key'],
        'app_key': module.params['app_key'],
    }
    initialize(**options)
    if (module.params['state'] == 'present'):
        install_monitor(module)
    elif (module.params['state'] == 'absent'):
        delete_monitor(module)
    elif (module.params['state'] == 'mute'):
        mute_monitor(module)
    elif (module.params['state'] == 'unmute'):
        unmute_monitor(module)