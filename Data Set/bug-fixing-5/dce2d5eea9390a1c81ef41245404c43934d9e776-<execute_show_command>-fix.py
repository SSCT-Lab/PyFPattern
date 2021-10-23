def execute_show_command(command, module):
    transport = module.params['transport']
    if (transport == 'cli'):
        if ('show run' not in command):
            command += ' | json'
    cmds = [command]
    body = run_commands(module, cmds)
    return body