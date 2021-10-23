def get_existing(module, args):
    existing = {
        
    }
    config = str(get_config(module))
    for arg in args:
        command = PARAM_TO_COMMAND_KEYMAP[arg]
        has_command = re.search('^{0}\\s(?P<value>.*)$'.format(command), config, re.M)
        value = ''
        if has_command:
            value = has_command.group('value')
        existing[arg] = value
    return existing