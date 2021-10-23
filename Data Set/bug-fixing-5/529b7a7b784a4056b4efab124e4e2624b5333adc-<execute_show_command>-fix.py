def execute_show_command(command, module, output='text'):
    command = {
        'command': command,
        'output': output,
    }
    return run_commands(module, [command])