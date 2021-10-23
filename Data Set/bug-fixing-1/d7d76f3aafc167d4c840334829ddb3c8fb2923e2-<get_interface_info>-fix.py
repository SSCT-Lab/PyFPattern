

def get_interface_info(interface, module):
    if (not interface.startswith('loopback')):
        interface = interface.capitalize()
    interface_type = get_interface_type(interface)
    intf_module = re.split('\\d+', interface)[0]
    intf_name = (interface_type + interface.split(intf_module)[1])
    command = 'show run | section interface.{0}'.format(interface)
    vrf_regex = '.*vrf\\s+member\\s+(?P<vrf>\\S+).*'
    try:
        body = execute_show_command(command, module, command_type='cli_show_ascii')[0]
        match_vrf = re.match(vrf_regex, body, re.DOTALL)
        group_vrf = match_vrf.groupdict()
        vrf = group_vrf['vrf']
    except (AttributeError, TypeError):
        return ''
    return vrf
