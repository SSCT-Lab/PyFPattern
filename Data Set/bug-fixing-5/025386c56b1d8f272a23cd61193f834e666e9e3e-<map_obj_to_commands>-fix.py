def map_obj_to_commands(want, have, module):
    commands = list()
    state = module.params['state']
    platform_regex = 'Nexus.*Switch'
    if (state == 'absent'):
        if (have.get('text') and (not ((have.get('text') == 'User Access Verification') or re.match(platform_regex, have.get('text'))))):
            commands.append(('no banner %s' % module.params['banner']))
    elif ((state == 'present') and (want.get('text') != have.get('text'))):
        banner_cmd = ('banner %s @\n%s\n@' % (module.params['banner'], want['text'].strip()))
        commands.append(banner_cmd)
    return commands