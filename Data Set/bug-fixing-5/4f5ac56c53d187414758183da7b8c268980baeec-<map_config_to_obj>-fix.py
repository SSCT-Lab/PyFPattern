def map_config_to_obj(module):
    command = ('show banner %s' % module.params['banner'])
    output = execute_show_command(module, command)[0]
    if ('Invalid command' in output):
        module.fail_json(msg='banner: exec may not be supported on this platform.  Possible values are : exec | motd')
    if isinstance(output, dict):
        output = list(output.values())
        if (output != []):
            output = output[0]
        else:
            output = ''
        if isinstance(output, dict):
            output = list(output.values())
            if (output != []):
                output = output[0]
            else:
                output = ''
    else:
        output = output.rstrip()
    obj = {
        'banner': module.params['banner'],
        'state': 'absent',
    }
    if output:
        obj['text'] = output
        obj['state'] = 'present'
    return obj