

def run(self, command, output='text'):
    command_string = command
    command = {
        'command': command,
        'output': output,
    }
    resp = run_commands(self.module, [command], check_rc=False)
    try:
        return resp[0]
    except IndexError:
        self.warnings.append(('command %s failed, facts will not be populated' % command_string))
        return None
