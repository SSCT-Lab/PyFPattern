def map_config_to_obj(module):
    obj = []
    output = run_commands(module, ['show interfaces ethernet'])
    lines = output[0].splitlines()
    if (len(lines) > 3):
        for line in lines[3:]:
            splitted_line = line.split()
            if (len(splitted_line) > 1):
                name = splitted_line[0]
                address = splitted_line[1]
                if (address == '-'):
                    address = None
                if ((address is not None) and (':' not in address)):
                    obj.append({
                        'name': name,
                        'ipv4': address,
                        'ipv6': None,
                    })
                else:
                    obj.append({
                        'name': name,
                        'ipv6': address,
                        'ipv4': None,
                    })
            else:
                obj[(- 1)]['ipv6'] = splitted_line[0]
    return obj