def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    state = module.params['state']
    if ((state == 'absent') and have['text']):
        commands.append(('no banner %s' % module.params['banner']))
    elif (state == 'present'):
        if (want['text'] and (want['text'] != have.get('text'))):
            if (module.params['transport'] == 'cli'):
                commands.append(('banner %s' % module.params['banner']))
                commands.extend(want['text'].strip().split('\n'))
                commands.append('EOF')
            else:
                commands.append({
                    'cmd': ('banner %s' % module.params['banner']),
                    'input': want['text'].strip('\n'),
                })
    return commands