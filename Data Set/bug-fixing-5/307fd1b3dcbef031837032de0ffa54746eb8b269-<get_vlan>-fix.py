def get_vlan(vlanid, module):
    'Get instance of VLAN as a dictionary\n    '
    command = ('show vlan id %s | json' % vlanid)
    try:
        body = run_commands(module, [command])[0]
        vlan_table = body['TABLE_vlanbriefid']['ROW_vlanbriefid']
    except (TypeError, IndexError, KeyError):
        return {
            
        }
    key_map = {
        'vlanshowbr-vlanid-utf': 'vlan_id',
        'vlanshowbr-vlanname': 'name',
        'vlanshowbr-vlanstate': 'vlan_state',
        'vlanshowbr-shutstate': 'admin_state',
    }
    vlan = apply_key_map(key_map, vlan_table)
    value_map = {
        'admin_state': {
            'shutdown': 'down',
            'noshutdown': 'up',
        },
    }
    vlan = apply_value_map(value_map, vlan)
    vlan['mapped_vni'] = get_vni(vlanid, module)
    return vlan