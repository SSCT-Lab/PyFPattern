def reboot(module):
    cmds = [{
        'command': 'terminal dont-ask',
        'output': 'text',
    }, {
        'command': 'reload',
        'output': 'text',
    }]
    run_commands(module, cmds)