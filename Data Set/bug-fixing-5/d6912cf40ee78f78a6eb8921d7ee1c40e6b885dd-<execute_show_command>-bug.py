def execute_show_command(command, module):
    provider = module.params['provider']
    if (provider['transport'] == 'cli'):
        if ('show port-channel summary' in command):
            command += ' | json'
        cmds = [command]
        body = run_commands(module, cmds)
    elif (provider['transport'] == 'nxapi'):
        cmds = [command]
        body = run_commands(module, cmds)
    return body