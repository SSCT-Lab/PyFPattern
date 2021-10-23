def get_vlan_config_commands(vlan, vid):
    'Build command list required for VLAN configuration\n    '
    reverse_value_map = {
        'admin_state': {
            'down': 'shutdown',
            'up': 'no shutdown',
        },
    }
    if vlan.get('admin_state'):
        vlan = apply_value_map(reverse_value_map, vlan)
    VLAN_ARGS = {
        'name': 'name {0}',
        'vlan_state': 'state {0}',
        'admin_state': '{0}',
        'mode': 'mode {0}',
        'mapped_vni': 'vn-segment {0}',
    }
    commands = []
    for (param, value) in vlan.items():
        if ((param == 'mapped_vni') and (value == 'default')):
            command = 'no vn-segment'
        else:
            command = VLAN_ARGS.get(param).format(vlan.get(param))
        if command:
            commands.append(command)
    commands.insert(0, ('vlan ' + vid))
    commands.append('exit')
    return commands