def exec_command(self, command):
    transform = ComplexDict(dict(command=dict(key=True), prompt=dict(), response=dict()))
    if (not isinstance(command, dict)):
        command = transform(command)
    (rc, out, err) = self.shell.send_command(command)
    return (rc, out, err)