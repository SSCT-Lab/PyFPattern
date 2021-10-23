

def map_config_to_obj(want, module):
    objs = list()
    for w in want:
        obj = dict(name=None, description=None, admin_state=None, speed=None, mtu=None, mode=None, duplex=None, interface_type=None, ip_forward=None, fabric_forwarding_anycast_gateway=None)
        if (not w['name']):
            return obj
        command = 'show interface {0}'.format(w['name'])
        try:
            body = execute_show_command(command, module)[0]
        except IndexError:
            return list()
        if body:
            try:
                interface_table = body['TABLE_interface']['ROW_interface']
            except KeyError:
                return list()
            if interface_table:
                if (interface_table.get('eth_mode') == 'fex-fabric'):
                    module.fail_json(msg='nxos_interface does not support interfaces with mode "fex-fabric"')
                intf_type = get_interface_type(w['name'])
                if (intf_type in ['portchannel', 'ethernet']):
                    if (not interface_table.get('eth_mode')):
                        obj['mode'] = 'layer3'
                if (intf_type == 'ethernet'):
                    obj['name'] = normalize_interface(interface_table.get('interface'))
                    obj['admin_state'] = interface_table.get('admin_state')
                    obj['description'] = interface_table.get('desc')
                    obj['mtu'] = interface_table.get('eth_mtu')
                    obj['duplex'] = interface_table.get('eth_duplex')
                    speed = interface_table.get('eth_speed')
                    mode = interface_table.get('eth_mode')
                    if (mode in ('access', 'trunk')):
                        obj['mode'] = 'layer2'
                    elif (mode in ('routed', 'layer3')):
                        obj['mode'] = 'layer3'
                    command = 'show run interface {0}'.format(obj['name'])
                    body = execute_show_command(command, module)[0]
                    if ('speed' in body):
                        obj['speed'] = re.search('speed (\\d+)', body).group(1)
                    else:
                        obj['speed'] = 'auto'
                    if ('duplex' in body):
                        obj['duplex'] = re.search('duplex (\\S+)', body).group(1)
                    else:
                        obj['duplex'] = 'auto'
                    if ('ip forward' in body):
                        obj['ip_forward'] = 'enable'
                    else:
                        obj['ip_forward'] = 'disable'
                elif (intf_type == 'svi'):
                    obj['name'] = normalize_interface(interface_table.get('interface'))
                    attributes = get_vlan_interface_attributes(obj['name'], intf_type, module)
                    obj['admin_state'] = str(attributes.get('admin_state', 'nxapibug'))
                    obj['description'] = str(attributes.get('description', 'nxapi_bug'))
                    command = 'show run interface {0}'.format(obj['name'])
                    body = execute_show_command(command, module)[0]
                    if ('ip forward' in body):
                        obj['ip_forward'] = 'enable'
                    else:
                        obj['ip_forward'] = 'disable'
                    if ('fabric forwarding mode anycast-gateway' in body):
                        obj['fabric_forwarding_anycast_gateway'] = True
                    else:
                        obj['fabric_forwarding_anycast_gateway'] = False
                elif (intf_type in ('loopback', 'management', 'nve')):
                    obj['name'] = normalize_interface(interface_table.get('interface'))
                    obj['admin_state'] = interface_table.get('admin_state')
                    obj['description'] = interface_table.get('desc')
                elif (intf_type == 'portchannel'):
                    obj['name'] = normalize_interface(interface_table.get('interface'))
                    obj['admin_state'] = interface_table.get('admin_state')
                    obj['description'] = interface_table.get('desc')
                    obj['mode'] = interface_table.get('eth_mode')
        objs.append(obj)
    return objs
