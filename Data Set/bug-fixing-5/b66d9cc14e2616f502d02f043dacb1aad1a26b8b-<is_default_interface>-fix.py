def is_default_interface(interface, module):
    'Checks to see if interface exists and if it is a default config\n    Args:\n        interface (str): full name of interface, i.e. vlan10,\n            Ethernet1/1, loopback10\n    Returns:\n        True: if interface has default config\n        False: if it does not have a default config\n        DNE (str): if the interface does not exist - loopbacks, SVIs, etc.\n    '
    command = ('show run interface ' + interface)
    try:
        body = run_commands(module, [command])[0]
    except IndexError:
        body = ''
    if body:
        raw_list = body.split('\n')
        found = False
        for line in raw_list:
            if line.startswith('interface'):
                found = True
            if (found and line and (not line.startswith('interface'))):
                return False
        return True
    else:
        return 'DNE'