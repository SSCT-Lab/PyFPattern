def map_config_to_obj(module):
    objs = []
    output = run_commands(module, ['show vlan'])
    lines = output[0].strip().splitlines()[2:]
    for l in lines:
        splitted_line = re.split('\\s{2,}', l.strip())
        obj = {
            
        }
        obj['vlan_id'] = splitted_line[0]
        obj['name'] = splitted_line[1]
        obj['state'] = splitted_line[2]
        if (obj['state'] == 'suspended'):
            obj['state'] = 'suspend'
        obj['interfaces'] = []
        if (len(splitted_line) > 3):
            for i in splitted_line[3].split(','):
                obj['interfaces'].append(i.strip().replace('Et', 'ethernet'))
        objs.append(obj)
    return objs