def parse_commands(module, warnings):
    command = ComplexList(dict(command=dict(key=True), prompt=dict(), answer=dict()), module)
    commands = command(module.params['commands'])
    for (index, item) in enumerate(commands):
        if (module.check_mode and (not item['command'].startswith('show'))):
            warnings.append(('only show commands are supported when using check mode, not executing `%s`' % item['command']))
        elif item['command'].startswith('conf'):
            module.fail_json(msg='aireos_command does not support running config mode commands.  Please use aireos_config instead')
    return commands