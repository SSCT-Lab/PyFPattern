

def map_config_to_obj(module):
    objs = list()
    output = None
    command = ['show vlan brief | json']
    output = run_commands(module, command, check_rc='retry_json')[0]
    if output:
        netcfg = CustomNetworkConfig(indent=2, contents=get_config(module, flags=['all']))
        if isinstance(output, dict):
            vlans = None
            try:
                vlans = output['TABLE_vlanbriefxbrief']['ROW_vlanbriefxbrief']
            except KeyError:
                return objs
            if vlans:
                if isinstance(vlans, list):
                    for vlan in vlans:
                        obj = parse_vlan_options(module, netcfg, output, vlan)
                        objs.append(obj)
                elif isinstance(vlans, dict):
                    obj = parse_vlan_options(module, netcfg, output, vlans)
                    objs.append(obj)
        else:
            vlans = list()
            splitted_line = re.split('\\n(\\d+)|\\n{2}', output.strip())
            for line in splitted_line:
                if (not line):
                    continue
                if (len(line) > 0):
                    line = line.strip()
                    if line[0].isdigit():
                        match = re.search('(\\d+)', line, re.M)
                        if match:
                            v = match.group(1)
                            pos1 = splitted_line.index(v)
                            pos2 = (pos1 + 1)
                            vlaninfo = ''.join(splitted_line[pos1:(pos2 + 1)])
                            vlans.append(vlaninfo)
            if vlans:
                objs = parse_vlan_non_structured(module, netcfg, vlans)
            else:
                return objs
    return objs
