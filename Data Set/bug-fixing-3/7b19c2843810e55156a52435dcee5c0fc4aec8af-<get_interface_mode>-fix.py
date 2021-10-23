def get_interface_mode(interface, intf_type, module):
    command = 'show interface {0}'.format(interface)
    interface = {
        
    }
    mode = 'unknown'
    if (intf_type in ['ethernet', 'portchannel']):
        body = execute_show_command(command, module)
        try:
            interface_table = body['TABLE_interface']['ROW_interface']
        except KeyError:
            return mode
        if (interface_table and isinstance(interface_table, dict)):
            mode = str(interface_table.get('eth_mode', 'layer3'))
            if ((mode == 'access') or (mode == 'trunk')):
                mode = 'layer2'
        else:
            return mode
    elif ((intf_type == 'loopback') or (intf_type == 'svi')):
        mode = 'layer3'
    return mode