

def reboot(module):
    cmds = [{
        'command': 'terminal-dont-ask',
    }, {
        'command': 'reload',
        'output': 'text',
    }]
    run_commands(module, cmds)
