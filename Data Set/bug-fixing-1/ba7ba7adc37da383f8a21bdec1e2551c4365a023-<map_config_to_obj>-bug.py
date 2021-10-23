

def map_config_to_obj(module):
    output = run_commands(module, [('show banner %s' % module.params['banner'])])
    obj = {
        'banner': module.params['banner'],
        'state': 'absent',
    }
    if output:
        if (module.params['transport'] == 'cli'):
            obj['text'] = output[0]
        elif (isinstance(output[0], dict) and ('loginBanner' in output[0].keys())):
            obj['text'] = output[0]['loginBanner'].strip('\n')
        obj['state'] = 'present'
    return obj
