

def map_config_to_obj(module):
    objs = []
    output = run_commands(module, {
        'command': 'show vrf',
        'output': 'text',
    })
    lines = output[0].strip().splitlines()[3:]
    out_len = len(lines)
    index = 0
    while (out_len > index):
        line = lines[index]
        if (not line):
            continue
        splitted_line = re.split('\\s{2,}', line.strip())
        if (len(splitted_line) == 1):
            index += 1
            continue
        else:
            obj = dict()
            obj['name'] = splitted_line[0]
            obj['rd'] = splitted_line[1]
            obj['interfaces'] = []
            if (len(splitted_line) > 4):
                obj['interfaces'] = []
                interfaces = splitted_line[4]
                if interfaces.endswith(','):
                    while interfaces.endswith(','):
                        if (out_len <= index):
                            break
                        index += 1
                        line = lines[index]
                        vrf_line = re.split('\\s{2,}', line.strip())
                        interfaces += vrf_line[(- 1)]
                for i in interfaces.split(','):
                    obj['interfaces'].append(i.strip().lower())
        index += 1
        objs.append(obj)
    return objs
