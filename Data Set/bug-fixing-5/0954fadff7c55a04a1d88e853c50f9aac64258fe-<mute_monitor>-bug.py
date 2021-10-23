def mute_monitor(module):
    monitor = _get_monitor(module)
    if (not monitor):
        module.fail_json(msg=('Monitor %s not found!' % module.params['name']))
    elif monitor['options']['silenced']:
        module.fail_json(msg='Monitor is already muted. Datadog does not allow to modify muted alerts, consider unmuting it first.')
    elif ((module.params['silenced'] is not None) and (len((set(monitor['options']['silenced']) - set(module.params['silenced']))) == 0)):
        module.exit_json(changed=False)
    try:
        if ((module.params['silenced'] is None) or (module.params['silenced'] == '')):
            msg = api.Monitor.mute(id=monitor['id'])
        else:
            msg = api.Monitor.mute(id=monitor['id'], silenced=module.params['silenced'])
        module.exit_json(changed=True, msg=msg)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=traceback.format_exc())