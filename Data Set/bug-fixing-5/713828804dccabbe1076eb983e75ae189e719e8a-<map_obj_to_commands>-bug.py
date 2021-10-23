def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    state = module.params['state']
    purge = module.params['purge']
    for w in want:
        name = w['name']
        description = w['description']
        vni = w['vni']
        rd = w['rd']
        admin_state = w['admin_state']
        interfaces = (w.get('interfaces') or [])
        state = w['state']
        del w['state']
        obj_in_have = search_obj_in_list(name, have)
        if ((state == 'absent') and obj_in_have):
            commands.append('no vrf context {0}'.format(name))
        elif (state == 'present'):
            if (not obj_in_have):
                commands.append('vrf context {0}'.format(name))
                if (rd and (rd != '')):
                    commands.append('rd {0}'.format(rd))
                if description:
                    commands.append('description {0}'.format(description))
                if (vni and (vni != '')):
                    commands.append('vni {0}'.format(vni))
                if (admin_state == 'up'):
                    commands.append('no shutdown')
                elif (admin_state == 'down'):
                    commands.append('shutdown')
                if commands:
                    if vni:
                        if (have.get('vni') and (have.get('vni') != '')):
                            commands.insert(1, 'no vni {0}'.format(have['vni']))
                commands.append('exit')
                if interfaces:
                    for i in interfaces:
                        commands.append('interface {0}'.format(i))
                        commands.append('no switchport')
                        commands.append('vrf member {0}'.format(name))
            elif interfaces:
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