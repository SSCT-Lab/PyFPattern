def get_value(arg, config, module):
    command = PARAM_TO_COMMAND_KEYMAP[arg]
    command_val_re = re.compile('(?:{0}\\s)(?P<value>.*)$'.format(command), re.M)
    has_command_val = command_val_re.search(config)
    if (arg == 'inject_map'):
        inject_re = '.*inject-map\\s(?P<inject_map>\\S+)\\sexist-map\\s(?P<exist_map>\\S+)-*'
        value = []
        match_inject = re.match(inject_re, config, re.DOTALL)
        if match_inject:
            inject_group = match_inject.groupdict()
            inject_map = inject_group['inject_map']
            exist_map = inject_group['exist_map']
            value.append(inject_map)
            value.append(exist_map)
            inject_map_command = 'inject-map {0} exist-map {1} copy-attributes'.format(inject_group['inject_map'], inject_group['exist_map'])
            inject_re = re.compile('\\s+{0}\\s*$'.format(inject_map_command), re.M)
            if inject_re.search(config):
                value.append('copy_attributes')
    elif (arg == 'networks'):
        value = []
        for network in command_val_re.findall(config):
            value.append(network.split())
    elif (arg == 'redistribute'):
        value = []
        if has_command_val:
            value = has_command_val.group('value').split()
            if value:
                if (len(value) == 3):
                    value.pop(1)
                elif (len(value) == 4):
                    value = ['{0} {1}'.format(value[0], value[1]), value[3]]
    elif (command == 'distance'):
        distance_re = '.*distance\\s(?P<d_ebgp>\\w+)\\s(?P<d_ibgp>\\w+)\\s(?P<d_local>\\w+)'
        match_distance = re.match(distance_re, config, re.DOTALL)
        value = ''
        if match_distance:
            distance_group = match_distance.groupdict()
            if (arg == 'distance_ebgp'):
                value = distance_group['d_ebgp']
            elif (arg == 'distance_ibgp'):
                value = distance_group['d_ibgp']
            elif (arg == 'distance_local'):
                value = distance_group['d_local']
    elif (command.split()[0] == 'dampening'):
        value = ''
        if ((arg == 'dampen_igp_metric') or (arg == 'dampening_routemap')):
            if (command in config):
                value = has_command_val.group('value')
        else:
            dampening_re = '.*dampening\\s(?P<half>\\w+)\\s(?P<reuse>\\w+)\\s(?P<suppress>\\w+)\\s(?P<max_suppress>\\w+)'
            match_dampening = re.match(dampening_re, config, re.DOTALL)
            if match_dampening:
                dampening_group = match_dampening.groupdict()
                if (arg == 'dampening_half_time'):
                    value = dampening_group['half']
                elif (arg == 'dampening_reuse_time'):
                    value = dampening_group['reuse']
                elif (arg == 'dampening_suppress_time'):
                    value = dampening_group['suppress']
                elif (arg == 'dampening_max_suppress_time'):
                    value = dampening_group['max_suppress']
    elif (arg == 'table_map_filter'):
        tmf_regex = re.compile('\\s+table-map.*filter$', re.M)
        value = False
        if tmf_regex.search(config):
            value = True
    elif (arg == 'table_map'):
        tm_regex = re.compile('(?:table-map\\s)(?P<value>\\S+)(\\sfilter)?$', re.M)
        has_tablemap = tm_regex.search(config)
        value = ''
        if has_tablemap:
            value = has_tablemap.group('value')
    elif (arg == 'client_to_client'):
        no_command_re = re.compile('^\\s+no\\s{0}\\s*$'.format(command), re.M)
        value = True
        if no_command_re.search(config):
            value = False
    elif (arg in BOOL_PARAMS):
        command_re = re.compile('^\\s+{0}\\s*$'.format(command), re.M)
        value = False
        if command_re.search(config):
            value = True
    else:
        value = ''
        if has_command_val:
            value = has_command_val.group('value')
    return value