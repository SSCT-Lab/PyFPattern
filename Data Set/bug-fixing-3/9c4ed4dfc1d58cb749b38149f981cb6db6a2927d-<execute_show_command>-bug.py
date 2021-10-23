def execute_show_command(module, command):
    format = 'json'
    cmds = [{
        'command': command,
        'output': format,
    }]
    output = run_commands(module, cmds, False)
    if ((len(output) == 0) or (len(output[0]) == 0)):
        cmds[0]['output'] = 'text'
        output = run_commands(module, cmds, False)
    return output