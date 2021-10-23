def execute_show_command(command, module, command_type='cli_show_ascii'):
    cmds = [command]
    if (module.params['transport'] == 'cli'):
        body = run_commands(module, cmds)
    elif (module.params['transport'] == 'nxapi'):
        body = run_commands(module, cmds)
    return body