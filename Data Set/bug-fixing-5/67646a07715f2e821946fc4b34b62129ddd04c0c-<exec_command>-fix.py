def exec_command(self, command):
    transform = ComplexDict(dict(command=dict(key=True), prompt=dict(), response=dict()))
    try:
        cmdobj = json.loads(command)
    except ValueError:
        cmdobj = transform(command)
    (rc, out, err) = self.shell.send_command(cmdobj)
    return (rc, out, err)