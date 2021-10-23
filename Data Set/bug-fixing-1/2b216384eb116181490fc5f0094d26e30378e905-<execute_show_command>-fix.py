

def execute_show_command(module, command):
    format = 'text'
    cmds = [{
        'command': command,
        'output': format,
    }]
    output = run_commands(module, cmds)
    return output
