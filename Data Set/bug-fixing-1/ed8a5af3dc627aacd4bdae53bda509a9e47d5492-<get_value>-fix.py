

def get_value(arg, config):
    command = PARAM_TO_COMMAND_KEYMAP.get(arg)
    if (command.split()[0] == 'event-history'):
        command_re = re.compile('\\s+{0}\\s*'.format(command), re.M)
        has_size = re.search('^\\s+{0} size\\s(?P<value>.*)$'.format(command), config, re.M)
        if (command == 'event-history detail'):
            value = False
        else:
            value = 'size_small'
        if command_re.search(config):
            if has_size:
                value = ('size_%s' % has_size.group('value'))
            else:
                value = True
    elif (arg in ['enforce_first_as', 'fast_external_fallover']):
        no_command_re = re.compile('no\\s+{0}\\s*'.format(command), re.M)
        value = True
        if no_command_re.search(config):
            value = False
    elif (arg in BOOL_PARAMS):
        has_command = re.search('^\\s+{0}\\s*$'.format(command), config, re.M)
        value = False
        if has_command:
            value = True
    else:
        command_val_re = re.compile('(?:{0}\\s)(?P<value>.*)'.format(command), re.M)
        value = ''
        has_command = command_val_re.search(config)
        if has_command:
            found_value = has_command.group('value')
            if (arg == 'confederation_peers'):
                value = found_value.split()
            elif (arg == 'timer_bgp_keepalive'):
                value = found_value.split()[0]
            elif (arg == 'timer_bgp_hold'):
                split_values = found_value.split()
                if (len(split_values) == 2):
                    value = split_values[1]
            elif found_value:
                value = found_value
    return value
