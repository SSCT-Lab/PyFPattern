def get_interface_info(interface, module):
    if (not interface.startswith('loopback')):
        interface = interface.capitalize()
    command = 'show run interface {0}'.format(interface)
    vrf_regex = '.*vrf\\s+member\\s+(?P<vrf>\\S+).*'
    try:
        body = execute_show_command(command, module)
        match_vrf = re.match(vrf_regex, body, re.DOTALL)
        group_vrf = match_vrf.groupdict()
        vrf = group_vrf['vrf']
    except (AttributeError, TypeError):
        return ''
    return vrf