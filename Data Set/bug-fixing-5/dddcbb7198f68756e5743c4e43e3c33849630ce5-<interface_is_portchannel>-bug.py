def interface_is_portchannel(name, module):
    if (get_interface_type(name) == 'ethernet'):
        config = get_config(module, flags=[' | section interface'])
        if ('channel group' in config):
            return True
    return False