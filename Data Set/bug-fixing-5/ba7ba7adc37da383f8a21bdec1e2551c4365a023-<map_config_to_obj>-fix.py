def map_config_to_obj(module):
    output = run_commands(module, [('show banner %s' % module.params['banner'])])
    obj = {
        'banner': module.params['banner'],
        'state': 'absent',
    }
    if output:
        if (module.params['transport'] == 'cli'):
            obj['text'] = output[0]
        else:
            if (module.params['banner'] == 'login'):
                banner_response_key = 'loginBanner'
            else:
                banner_response_key = 'motd'
            if (isinstance(output[0], dict) and (banner_response_key in output[0].keys())):
                obj['text'] = output[0][banner_response_key].strip('\n')
        obj['state'] = 'present'
    return obj