def get_interface(intf, module):
    'Gets current config/state of interface\n    Args:\n        intf (string): full name of interface, i.e. Ethernet1/1, loopback10,\n            port-channel20, vlan20\n    Returns:\n      dictionary that has relevant config/state data about the given\n          interface based on the type of interface it is\n    '
    base_key_map = {
        'interface': 'interface',
        'admin_state': 'admin_state',
        'desc': 'description',
    }
    mode_map = {
        'eth_mode': 'mode',
    }
    loop_map = {
        'state': 'admin_state',
    }
    svi_map = {
        'svi_admin_state': 'admin_state',
        'desc': 'description',
    }
    mode_value_map = {
        'mode': {
            'access': 'layer2',
            'trunk': 'layer2',
            'routed': 'layer3',
            'layer3': 'layer3',
        },
    }
    key_map = {
        
    }
    interface = {
        
    }
    command = 'show interface {0}'.format(intf)
    try:
        body = execute_show_command(command, module)[0]
    except IndexError:
        body = []
    if body:
        interface_table = body['TABLE_interface']['ROW_interface']
        intf_type = get_interface_type(intf)
        if (intf_type in ['portchannel', 'ethernet']):
            if (not interface_table.get('eth_mode')):
                interface_table['eth_mode'] = 'layer3'
        if (intf_type == 'ethernet'):
            key_map.update(base_key_map)
            key_map.update(mode_map)
            temp_dict = apply_key_map(key_map, interface_table)
            temp_dict = apply_value_map(mode_value_map, temp_dict)
            interface.update(temp_dict)
        elif (intf_type == 'svi'):
            key_map.update(svi_map)
            temp_dict = apply_key_map(key_map, interface_table)
            interface.update(temp_dict)
            attributes = get_manual_interface_attributes(intf, module)
            interface['admin_state'] = str(attributes.get('admin_state', 'nxapibug'))
            interface['description'] = str(attributes.get('description', 'nxapi_bug'))
            command = 'show run interface {0}'.format(intf)
            body = execute_show_command(command, module)[0]
            if ('ip forward' in body):
                interface['ip_forward'] = 'enable'
            else:
                interface['ip_forward'] = 'disable'
            if ('fabric forwarding mode anycast-gateway' in body):
                interface['fabric_forwarding_anycast_gateway'] = True
            else:
                interface['fabric_forwarding_anycast_gateway'] = False
        elif (intf_type == 'loopback'):
            key_map.update(base_key_map)
            key_map.pop('admin_state')
            key_map.update(loop_map)
            temp_dict = apply_key_map(key_map, interface_table)
            if (not temp_dict.get('description')):
                temp_dict['description'] = 'None'
            interface.update(temp_dict)
        elif (intf_type == 'management'):
            key_map.update(base_key_map)
            temp_dict = apply_key_map(key_map, interface_table)
            interface.update(temp_dict)
        elif (intf_type == 'portchannel'):
            key_map.update(base_key_map)
            key_map.update(mode_map)
            temp_dict = apply_key_map(key_map, interface_table)
            temp_dict = apply_value_map(mode_value_map, temp_dict)
            if (not temp_dict.get('description')):
                temp_dict['description'] = 'None'
            interface.update(temp_dict)
        elif (intf_type == 'nve'):
            key_map.update(base_key_map)
            temp_dict = apply_key_map(key_map, interface_table)
            if (not temp_dict.get('description')):
                temp_dict['description'] = 'None'
            interface.update(temp_dict)
    interface['type'] = intf_type
    return interface