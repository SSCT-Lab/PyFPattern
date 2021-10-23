def get_manual_interface_attributes(interface, module):
    'Gets admin state and description of a SVI interface. Hack due to API.\n    Args:\n        interface (str): full name of SVI interface, i.e. vlan10\n    Returns:\n        dictionary that has two k/v pairs: admin_state & description\n            if not an svi, returns None\n    '
    if (get_interface_type(interface) == 'svi'):
        command = 'show interface {0}'.format(interface)
        try:
            body = execute_show_command(command, module)[0]
        except IndexError:
            return None
        command_list = body.split('\n')
        desc = None
        admin_state = 'up'
        for each in command_list:
            if ('Description:' in each):
                line = each.split('Description:')
                desc = line[1].strip().split('MTU')[0].strip()
            elif ('Administratively down' in each):
                admin_state = 'down'
        return dict(description=desc, admin_state=admin_state)
    else:
        return None