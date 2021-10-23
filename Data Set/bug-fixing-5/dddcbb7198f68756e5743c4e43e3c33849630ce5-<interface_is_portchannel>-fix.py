def interface_is_portchannel(name, module):
    if (get_interface_type(name) == 'ethernet'):
        config = run_commands(module, ['show run interface {0}'.format(name)])[0]
        if any(((c in config) for c in ['channel group', 'channel-group'])):
            return True
    return False