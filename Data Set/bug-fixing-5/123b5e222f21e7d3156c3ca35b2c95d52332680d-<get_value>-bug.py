def get_value(arg, config):
    command = PARAM_TO_COMMAND_KEYMAP[arg]
    has_command = re.search('\\s+{0}\\s*$'.format(command), config, re.M)
    has_command_value = re.search('(?:{0}\\s)(?P<value>.*)$'.format(command), config, re.M)
    if (arg in BOOL_PARAMS):
        value = False
        try:
            if has_command:
                value = True
        except TypeError:
            value = False
    elif (arg == 'log_neighbor_changes'):
        value = ''
        if has_command:
            if has_command_value:
                value = 'disable'
            else:
                value = 'enable'
    elif (arg == 'remove_private_as'):
        value = 'disable'
        if has_command:
            if has_command_value:
                value = has_command_value.group('value')
            else:
                value = 'enable'
    else:
        value = ''
        if has_command_value:
            value = has_command_value.group('value')
            if (command in ['timers', 'password']):
                split_value = value.split()
                value = ''
                if (arg in ['timers_keepalive', 'pwd_type']):
                    value = split_value[0]
                elif ((arg in ['timers_holdtime', 'pwd']) and (len(split_value) == 2)):
                    value = split_value[1]
    return value