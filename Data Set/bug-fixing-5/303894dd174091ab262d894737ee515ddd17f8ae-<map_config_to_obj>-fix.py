def map_config_to_obj(module):
    output = run_commands(module, [('show banner %s' % module.params['banner'])], False)[0]
    if ('Invalid command' in output):
        module.fail_json(msg='banner: exec may not be supported on this platform.  Possible values are : exec | motd')
    if isinstance(output, dict):
        output = list(output.values())[0]
        if isinstance(output, dict):
            output = list(output.values())[0]
    obj = {
        'banner': module.params['banner'],
        'state': 'absent',
    }
    if output:
        obj['text'] = output
        obj['state'] = 'present'
    return obj