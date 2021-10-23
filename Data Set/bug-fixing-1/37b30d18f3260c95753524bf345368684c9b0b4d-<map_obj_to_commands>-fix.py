

def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    purge = module.params['purge']
    for w in want:
        vlan_id = w['vlan_id']
        name = w['name']
        address = w['address']
        state = w['state']
        obj_in_have = search_obj_in_list(vlan_id, have)
        if (state == 'absent'):
            if obj_in_have:
                for obj in obj_in_have:
                    for i in obj['interfaces']:
                        commands.append('delete interfaces ethernet {0} vif {1}'.format(i, vlan_id))
        elif (state == 'present'):
            if (not obj_in_have):
                if (w['interfaces'] and w['vlan_id']):
                    for i in w['interfaces']:
                        cmd = 'set interfaces ethernet {0} vif {1}'.format(i, vlan_id)
                        if w['name']:
                            commands.append((cmd + ' description {0}'.format(name)))
                        elif w['address']:
                            commands.append((cmd + ' address {0}'.format(address)))
                        else:
                            commands.append(cmd)
    if purge:
        for h in have:
            obj_in_want = search_obj_in_list(h['vlan_id'], want)
            if (not obj_in_want):
                for i in h['interfaces']:
                    commands.append('delete interfaces ethernet {0} vif {1}'.format(i, h['vlan_id']))
    return commands
