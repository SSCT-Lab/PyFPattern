def execute_show_command(command, module):
    cmds = [{
        'command': command,
        'output': 'text',
    }]
    return run_commands(module, cmds)