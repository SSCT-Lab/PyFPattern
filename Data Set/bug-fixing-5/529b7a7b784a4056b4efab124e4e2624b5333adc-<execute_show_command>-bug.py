def execute_show_command(command, module):
    command = {
        'command': command,
        'output': 'text',
    }
    return run_commands(module, [command])