def execute_show_command(command, module, command_type='cli_show'):
    if (command_type == 'cli_show_ascii'):
        cmds = [{
            'command': command,
            'output': 'text',
        }]
    else:
        cmds = [command]
    return run_commands(module, cmds)