

def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    state = module.params['state']
    purge = module.params['purge']
    args = ('rd', 'description', 'vni')
    for w in want:
        name = w['name']
        admin_state = w['admin_state']
        vni = w['vni']
        interfaces = (w.get('interfaces') or [])
        state = w['state']
        del w['state']
        obj_in_have = search_obj_in_list(name, have)
        if ((state == 'absent') and obj_in_have):
            commands.append('no vrf context {0}'.format(name))
        elif (state == 'present'):
            if (not obj_in_have):
                commands.append('vrf context {0}'.format(name))
                for item in args:
                    candidate = w.get(item)
                    if candidate:
                        cmd = ((item + ' ') + str(candidate))
                        commands.append(cmd)
                if (admin_state == 'up'):
                    commands.append('no shutdown')
                elif (admin_state == 'down'):
                    commands.append('shutdown')
                commands.append('exit')
                if interfaces:
                    for i in interfaces:
                        commands.append('interface {0}'.format(i))
                        commands.append('no switchport')
                        commands.append('vrf member {0}'.format(name))
            else:
                if vni:
                    if (obj_in_have.get('vni') and (vni != obj_in_have.get('vni'))):
                        commands.append('no vni {0}'.format(obj_in_have.get('vni')))
                for item in args:
                    candidate = w.get(item)
                    if (candidate and (candidate != obj_in_have.get(item))):
                        cmd = ((item + ' ') + str(candidate))
                        commands.append(cmd)
                if (admin_state and (admin_state != obj_in_have.get('admin_state'))):
                    if (admin_state == 'up'):
                        commands.append('no shutdown')
                    elif (admin_state == 'down'):
                        commands.append('shutdown')
                if commands:
                    commands.insert(0, 'vrf context {0}'.format(name))
                    commands.append('exit')
                if interfaces:
                    if (not obj_in_have['interfaces']):
                        for i in interfaces:
                            commands.append('vrf context {0}'.format(name))
                            commands.append('exit')
                            commands.append('interface {0}'.format(i))
                            commands.append('no switchport')
                            commands.append('vrf member {0}'.format(name))
                    elif (set(interfaces) != set(obj_in_have['interfaces'])):
                        missing_interfaces = list((set(interfaces) - set(obj_in_have['interfaces'])))
                        for i in missing_interfaces:
                            commands.append('vrf context {0}'.format(name))
                            commands.append('exit')
                            commands.append('interface {0}'.format(i))
                            commands.append('no switchport')
                            commands.append('vrf member {0}'.format(name))
                        superfluous_interfaces = list((set(obj_in_have['interfaces']) - set(interfaces)))
                        for i in superfluous_interfaces:
                            commands.append('vrf context {0}'.format(name))
                            commands.append('exit')
                            commands.append('interface {0}'.format(i))
                            commands.append('no switchport')
                            commands.append('no vrf member {0}'.format(name))
    if purge:
        existing = get_existing_vrfs(module)
        if existing:
            for h in existing:
                if (h['name'] in ('default', 'management')):
                    pass
                else:
                    obj_in_want = search_obj_in_list(h['name'], want)
                    if (not obj_in_want):
                        commands.append('no vrf context {0}'.format(h['name']))
    return commands
