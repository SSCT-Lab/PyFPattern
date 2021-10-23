def exec_command(self, command):
    try:
        cmdobj = json.loads(command)
        return self.shell.send_command(cmdobj)
    except ValueError:
        return (1, '', 'unable to parse request')