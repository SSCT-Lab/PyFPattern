

def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    purge = module.params['purge']
    for w in want:
        group = w['group']
        mode = w['mode']
        members = (w.get('members') or [])
        state = w['state']
        del w['state']
        obj_in_have = search_obj_in_list(group, have)
        if (state == 'absent'):
            if obj_in_have:
                commands.append('no interface port-channel {0}'.format(group))
        elif (state == 'present'):
            cmd = ['interface port-channel {0}'.format(group), 'exit']
            if (not obj_in_have):
                if (not group):
                    module.fail_json(msg='group is a required option')
                commands.extend(cmd)
                if members:
                    for m in members:
                        commands.append('interface {0}'.format(m))
                        commands.append('channel-group {0} mode {1}'.format(group, mode))
            elif members:
                if ('members' not in obj_in_have.keys()):
                    for m in members:
                        commands.extend(cmd)
                        commands.append('interface {0}'.format(m))
                        commands.append('channel-group {0} mode {1}'.format(group, mode))
                elif (set(members) != set(obj_in_have['members'])):
                    missing_members = list((set(members) - set(obj_in_have['members'])))
                    for m in missing_members:
                        commands.extend(cmd)
                        commands.append('interface {0}'.format(m))
                        commands.append('channel-group {0} mode {1}'.format(group, mode))
                    superfluous_members = list((set(obj_in_have['members']) - set(members)))
                    for m in superfluous_members:
                        commands.extend(cmd)
                        commands.append('interface {0}'.format(m))
                        commands.append('no channel-group {0} mode {1}'.format(group, mode))
    if purge:
        for h in have:
            obj_in_want = search_obj_in_list(h['group'], want)
            if (not obj_in_want):
                commands.append('no interface port-channel {0}'.format(h['group']))
    return commands
