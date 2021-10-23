def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    for w in want:
        name = w['name']
        ipv4 = w['ipv4']
        ipv6 = w['ipv6']
        state = w['state']
        obj_in_have = search_obj_in_list(name, have)
        if ((state == 'absent') and obj_in_have):
            if ((not ipv4) and (not ipv6) and (obj_in_have['ipv4'] or obj_in_have['ipv6'])):
                if (name == 'lo'):
                    commands.append('delete interfaces loopback lo address')
                else:
                    commands.append((('delete interfaces ethernet ' + name) + ' address'))
            else:
                if (ipv4 and obj_in_have['ipv4']):
                    if (name == 'lo'):
                        commands.append(('delete interfaces loopback lo address ' + ipv4))
                    else:
                        commands.append(((('delete interfaces ethernet ' + name) + ' address ') + ipv4))
                if (ipv6 and obj_in_have['ipv6']):
                    if (name == 'lo'):
                        commands.append(('delete interfaces loopback lo address ' + ipv6))
                    else:
                        commands.append(((('delete interfaces ethernet ' + name) + ' address ') + ipv6))
        elif ((state == 'present') and obj_in_have):
            if (ipv4 and (ipv4 != obj_in_have['ipv4'])):
                if (name == 'lo'):
                    commands.append(('set interfaces loopback lo address ' + ipv4))
                else:
                    commands.append(((('set interfaces ethernet ' + name) + ' address ') + ipv4))
            if (ipv6 and (ipv6 != obj_in_have['ipv6'])):
                if (name == 'lo'):
                    commands.append(('set interfaces loopback lo address ' + ipv6))
                else:
                    commands.append(((('set interfaces ethernet ' + name) + ' address ') + ipv6))
    return commands