def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    purge = module.params['purge']
    force = module.params['force']
    for w in want:
        group = w['group']
        mode = w['mode']
        min_links = w['min_links']
        members = (w.get('members') or [])
        state = w['state']
        del w['state']
        obj_in_have = search_obj_in_list(group, have)
        if (state == 'absent'):
            if obj_in_have:
                members_to_remove = list((set(obj_in_have['members']) - set(members)))
                if members_to_remove:
                    for m in members_to_remove:
                        commands.append('interface {0}'.format(m))
                        commands.append('no channel-group {0}'.format(obj_in_have['group']))
                        commands.append('exit')
                commands.append('no interface port-channel {0}'.format(group))
        elif (state == 'present'):
            if (not obj_in_have):
                commands.append('interface port-channel {0}'.format(group))
                if (min_links != 'None'):
                    commands.append('lacp min-links {0}'.format(min_links))
                commands.append('exit')
                if members:
                    for m in members:
                        commands.append('interface {0}'.format(m))
                        if force:
                            commands.append('channel-group {0} force mode {1}'.format(group, mode))
                        else:
                            commands.append('channel-group {0} mode {1}'.format(group, mode))
            elif members:
                if (not obj_in_have['members']):
                    for m in members:
                        commands.append('interface port-channel {0}'.format(group))
                        commands.append('exit')
                        commands.append('interface {0}'.format(m))
                        if force:
                            commands.append('channel-group {0} force mode {1}'.format(group, mode))
                        else:
                            commands.append('channel-group {0} mode {1}'.format(group, mode))
                elif (set(members) != set(obj_in_have['members'])):
                    missing_members = list((set(members) - set(obj_in_have['members'])))
                    for m in missing_members:
                        commands.append('interface port-channel {0}'.format(group))
                        commands.append('exit')
                        commands.append('interface {0}'.format(m))
                        if force:
                            commands.append('channel-group {0} force mode {1}'.format(group, mode))
                        else:
                            commands.append('channel-group {0} mode {1}'.format(group, mode))
                    superfluous_members = list((set(obj_in_have['members']) - set(members)))
                    for m in superfluous_members:
                        commands.append('interface port-channel {0}'.format(group))
                        commands.append('exit')
                        commands.append('interface {0}'.format(m))
                        commands.append('no channel-group {0}'.format(group))
    if purge:
        for h in have:
            obj_in_want = search_obj_in_list(h['group'], want)
            if (not obj_in_want):
                commands.append('no interface port-channel {0}'.format(h['group']))
    return commands