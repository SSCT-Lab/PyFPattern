def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    purge = module.params['purge']
    for w in want:
        vlan_id = w['vlan_id']
        name = w['name']
        state = w['state']
        interfaces = w['interfaces']
        obj_in_have = search_obj_in_list(vlan_id, have)
        if (state == 'absent'):
            if obj_in_have:
                commands.append(('no vlan %s' % w['vlan_id']))
        elif (state == 'present'):
            if (not obj_in_have):
                commands.append(('vlan %s' % w['vlan_id']))
                commands.append(('name %s' % w['name']))
                if w['interfaces']:
                    for i in w['interfaces']:
                        commands.append(('interface %s' % i))
                        commands.append(('switchport access vlan %s' % w['vlan_id']))
            else:
                if (w['name'] and (w['name'] != obj_in_have['name'])):
                    commands.append(('vlan %s' % w['vlan_id']))
                    commands.append(('name %s' % w['name']))
                if w['interfaces']:
                    if (not obj_in_have['interfaces']):
                        for i in w['interfaces']:
                            commands.append(('vlan %s' % w['vlan_id']))
                            commands.append(('interface %s' % i))
                            commands.append(('switchport access vlan %s' % w['vlan_id']))
                    elif (set(w['interfaces']) != obj_in_have['interfaces']):
                        missing_interfaces = list((set(w['interfaces']) - set(obj_in_have['interfaces'])))
                        for i in missing_interfaces:
                            commands.append(('vlan %s' % w['vlan_id']))
                            commands.append(('interface %s' % i))
                            commands.append(('switchport access vlan %s' % w['vlan_id']))
                        superfluous_interfaces = list((set(obj_in_have['interfaces']) - set(w['interfaces'])))
                        for i in superfluous_interfaces:
                            commands.append(('vlan %s' % w['vlan_id']))
                            commands.append(('interface %s' % i))
                            commands.append(('no switchport access vlan %s' % w['vlan_id']))
        elif (not obj_in_have):
            commands.append(('vlan %s' % w['vlan_id']))
            commands.append(('name %s' % w['name']))
            commands.append(('state %s' % w['state']))
        elif ((obj_in_have['name'] != w['name']) or (obj_in_have['state'] != w['state'])):
            commands.append(('vlan %s' % w['vlan_id']))
            if (obj_in_have['name'] != w['name']):
                commands.append(('name %s' % w['name']))
            if (obj_in_have['state'] != w['state']):
                commands.append(('state %s' % w['state']))
    if purge:
        for h in have:
            obj_in_want = search_obj_in_list(h['vlan_id'], want)
            if ((not obj_in_want) and (h['vlan_id'] != '1')):
                commands.append(('no vlan %s' % h['vlan_id']))
    return commands