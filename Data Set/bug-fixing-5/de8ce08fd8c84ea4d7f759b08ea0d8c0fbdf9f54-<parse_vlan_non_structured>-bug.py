def parse_vlan_non_structured(module, netcfg, vlans):
    objs = list()
    for vlan in vlans:
        vlan_match = re.search('(\\d+)', vlan, re.M)
        if vlan_match:
            obj = {
                
            }
            vlan_id = vlan_match.group(1)
            obj['vlan_id'] = str(vlan_id)
            name_match = re.search('{0}\\s*(\\S+)'.format(vlan_id), vlan, re.M)
            if name_match:
                name = name_match.group(1)
                obj['name'] = name
                state_match = re.search('{0}\\s*{1}\\s*(\\S+)'.format(vlan_id, name), vlan, re.M)
                if state_match:
                    vlan_state_match = state_match.group(1)
                    if (vlan_state_match == 'suspended'):
                        vlan_state = 'suspend'
                        admin_state = 'up'
                    elif (vlan_state_match == 'sus/lshut'):
                        vlan_state = 'suspend'
                        admin_state = 'down'
                    if (vlan_state_match == 'active'):
                        vlan_state = 'active'
                        admin_state = 'up'
                    if (vlan_state_match == 'act/lshut'):
                        vlan_state = 'active'
                        admin_state = 'down'
                    obj['vlan_state'] = vlan_state
                    obj['admin_state'] = admin_state
                    vlan = ','.join(vlan.splitlines())
                    interfaces = list()
                    intfs_match = re.search('{0}\\s*{1}\\s*{2}\\s*(.*)'.format(vlan_id, name, vlan_state_match), vlan, re.M)
                    if intfs_match:
                        intfs = intfs_match.group(1)
                        intfs = intfs.split()
                        for i in intfs:
                            intf = normalize_interface(i.strip(','))
                            interfaces.append(intf)
                    if interfaces:
                        obj['interfaces'] = interfaces
                    else:
                        obj['interfaces'] = None
                    config = parse_vlan_config(netcfg, vlan_id)
                    obj['mode'] = parse_mode(config)
                    obj['mapped_vni'] = parse_vni(config)
        objs.append(obj)
    return objs