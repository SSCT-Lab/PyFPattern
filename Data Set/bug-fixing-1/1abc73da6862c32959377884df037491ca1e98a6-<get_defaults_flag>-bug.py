

def get_defaults_flag(module):
    (rc, out, err) = exec_command(module, 'show running-config ?')
    commands = set()
    for line in out.splitlines():
        if line:
            commands.add(line.strip().split()[0])
    return ('all' if ('all' in commands) else 'full')
