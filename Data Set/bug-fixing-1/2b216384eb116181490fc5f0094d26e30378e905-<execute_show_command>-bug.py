

def execute_show_command(module, command):
    format = 'json'
    cmds = [{
        'command': command,
        'output': format,
    }]
    output = run_commands(module, cmds, check_rc='retry_json')
    return output
