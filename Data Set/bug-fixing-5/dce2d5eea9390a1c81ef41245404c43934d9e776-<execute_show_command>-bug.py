def execute_show_command(command, module, command_type='cli_show'):
    transport = module.params['provider']['transport']
    if (transport in ['cli', None]):
        if ('show run' not in command):
            command += ' | json'
        cmds = [command]
        body = run_commands(module, cmds)
    else:
        cmds = [command]
        body = run_commands(module, cmds)
    return body