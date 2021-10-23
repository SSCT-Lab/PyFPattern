def map_obj_to_commands(want, have, module):
    commands = list()
    state = module.params['state']
    if ((state == 'absent') and (have.get('text') and (have.get('text') != 'User Access Verification'))):
        commands.append(('no banner %s' % module.params['banner']))
    elif ((state == 'present') and (want.get('text') != have.get('text'))):
        banner_cmd = ('banner %s @\n%s\n@' % (module.params['banner'], want['text'].strip()))
        commands.append(banner_cmd)
    return commands