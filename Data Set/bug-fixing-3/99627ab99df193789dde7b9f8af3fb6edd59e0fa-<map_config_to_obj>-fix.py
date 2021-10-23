def map_config_to_obj(module):
    objs = []
    vlans = run_commands(module, ['show vlan conf | json'])
    for vlan in vlans[0]['vlans']:
        obj = {
            
        }
        obj['vlan_id'] = vlan
        obj['name'] = vlans[0]['vlans'][vlan]['name']
        obj['state'] = vlans[0]['vlans'][vlan]['status']
        obj['interfaces'] = []
        interfaces = vlans[0]['vlans'][vlan]
        for interface in interfaces['interfaces']:
            obj['interfaces'].append(interface)
        if (obj['state'] == 'suspended'):
            obj['state'] = 'suspend'
        objs.append(obj)
    return objs