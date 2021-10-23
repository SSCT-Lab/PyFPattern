def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    for w in want:
        name = w['name']
        ipv4 = w['ipv4']
        ipv6 = w['ipv6']
        state = w['state']
        interface = ('interface ' + name)
        commands.append(interface)
        obj_in_have = search_obj_in_list(name, have)
        if ((state == 'absent') and obj_in_have):
            if obj_in_have['ipv4']:
                if ipv4:
                    address = ipv4.split('/')
                    if (len(address) == 2):
                        ipv4 = '{0} {1}'.format(address[0], to_netmask(address[1]))
                    commands.append('no ip address {}'.format(ipv4))
                else:
                    commands.append('no ip address')
            if obj_in_have['ipv6']:
                if ipv6:
                    commands.append('no ipv6 address {}'.format(ipv6))
                else:
                    commands.append('no ipv6 address')
        elif (state == 'present'):
            if ipv4:
                if ((obj_in_have is None) or (obj_in_have.get('ipv4') is None) or (ipv4 != obj_in_have['ipv4'])):
                    address = ipv4.split('/')
                    if (len(address) == 2):
                        ipv4 = '{0} {1}'.format(address[0], to_netmask(address[1]))
                    commands.append('ip address {}'.format(ipv4))
            if ipv6:
                if ((obj_in_have is None) or (obj_in_have.get('ipv6') is None) or (ipv6.lower() != obj_in_have['ipv6'].lower())):
                    commands.append('ipv6 address {}'.format(ipv6))
        if (commands[(- 1)] == interface):
            commands.pop((- 1))
    return commands