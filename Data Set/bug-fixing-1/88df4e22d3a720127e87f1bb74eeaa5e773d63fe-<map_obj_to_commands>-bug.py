

def map_obj_to_commands(updates, module):
    commands = list()
    purge = module.params['purge']
    (want, have) = updates
    for w in want:
        vlan_id = w['vlan_id']
        name = w['name']
        interfaces = (w.get('interfaces') or [])
        mapped_vni = w['mapped_vni']
        mode = w['mode']
        vlan_state = w['vlan_state']
        admin_state = w['admin_state']
        state = w['state']
        del w['state']
        obj_in_have = search_obj_in_list(vlan_id, have)
        if (state == 'absent'):
            if obj_in_have:
                if (obj_in_have['mapped_vni'] != 'None'):
                    commands.append('vlan {0}'.format(vlan_id))
                    commands.append('no vn-segment')
                    commands.append('exit')
                commands.append('no vlan {0}'.format(vlan_id))
        elif (state == 'present'):
            if (not obj_in_have):
                commands.append('vlan {0}'.format(vlan_id))
                if (name and (name != 'default')):
                    commands.append('name {0}'.format(name))
                if mode:
                    commands.append('mode {0}'.format(mode))
                if vlan_state:
                    commands.append('state {0}'.format(vlan_state))
                if ((mapped_vni != 'None') and (mapped_vni != 'default')):
                    commands.append('vn-segment {0}'.format(mapped_vni))
                if (admin_state == 'up'):
                    commands.append('no shutdown')
                if (admin_state == 'down'):
                    commands.append('shutdown')
                commands.append('exit')
                if (interfaces and (interfaces[0] != 'default')):
                    for i in interfaces:
                        commands.append('interface {0}'.format(i))
                        commands.append('switchport')
                        commands.append('switchport mode access')
                        commands.append('switchport access vlan {0}'.format(vlan_id))
            else:
                diff = get_diff(w, obj_in_have)
                if diff:
                    commands.append('vlan {0}'.format(vlan_id))
                    for (key, value) in diff.items():
                        if (key == 'name'):
                            if (name != 'default'):
                                if (name is not None):
                                    commands.append('name {0}'.format(value))
                            elif (not is_default_name(obj_in_have, vlan_id)):
                                commands.append('no name')
                        if ((key == 'vlan_state') and value):
                            commands.append('state {0}'.format(value))
                        if (key == 'mapped_vni'):
                            if (value == 'default'):
                                if (obj_in_have['mapped_vni'] != 'None'):
                                    commands.append('no vn-segment')
                            elif (value != 'None'):
                                commands.append('vn-segment {0}'.format(value))
                        if (key == 'admin_state'):
                            if (value == 'up'):
                                commands.append('no shutdown')
                            elif (value == 'down'):
                                commands.append('shutdown')
                        if ((key == 'mode') and value):
                            commands.append('mode {0}'.format(value))
                    if (len(commands) > 1):
                        commands.append('exit')
                    else:
                        del commands[:]
                if (interfaces and (interfaces[0] != 'default')):
                    if (not obj_in_have['interfaces']):
                        for i in interfaces:
                            commands.append('vlan {0}'.format(vlan_id))
                            commands.append('exit')
                            commands.append('interface {0}'.format(i))
                            commands.append('switchport')
                            commands.append('switchport mode access')
                            commands.append('switchport access vlan {0}'.format(vlan_id))
                    elif (set(interfaces) != set(obj_in_have['interfaces'])):
                        missing_interfaces = list((set(interfaces) - set(obj_in_have['interfaces'])))
                        for i in missing_interfaces:
                            commands.append('vlan {0}'.format(vlan_id))
                            commands.append('exit')
                            commands.append('interface {0}'.format(i))
                            commands.append('switchport')
                            commands.append('switchport mode access')
                            commands.append('switchport access vlan {0}'.format(vlan_id))
                        superfluous_interfaces = list((set(obj_in_have['interfaces']) - set(interfaces)))
                        for i in superfluous_interfaces:
                            commands.append('vlan {0}'.format(vlan_id))
                            commands.append('exit')
                            commands.append('interface {0}'.format(i))
                            commands.append('switchport')
                            commands.append('switchport mode access')
                            commands.append('no switchport access vlan {0}'.format(vlan_id))
                elif (interfaces and (interfaces[0] == 'default')):
                    if obj_in_have['interfaces']:
                        for i in obj_in_have['interfaces']:
                            commands.append('vlan {0}'.format(vlan_id))
                            commands.append('exit')
                            commands.append('interface {0}'.format(i))
                            commands.append('switchport')
                            commands.append('switchport mode access')
                            commands.append('no switchport access vlan {0}'.format(vlan_id))
    if purge:
        for h in have:
            obj_in_want = search_obj_in_list(h['vlan_id'], want)
            if (not obj_in_want):
                commands.append('no vlan {0}'.format(h['vlan_id']))
    return commands
