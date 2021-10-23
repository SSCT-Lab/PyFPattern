def execute_show_command(command, module):
    device_info = get_capabilities(module)
    network_api = device_info.get('network_api', 'nxapi')
    if (network_api == 'cliconf'):
        if ('show port-channel summary' in command):
            command += ' | json'
        cmds = [command]
        body = run_commands(module, cmds)
    elif (network_api == 'nxapi'):
        cmds = [command]
        body = run_commands(module, cmds)
    return body