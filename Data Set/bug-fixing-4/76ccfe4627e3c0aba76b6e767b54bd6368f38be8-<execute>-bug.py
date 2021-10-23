def execute(self, commands):
    try:
        return self.shell.send(commands)
    except ShellError:
        exc = get_exception()
        commands = [str(c) for c in commands]
        raise NetworkError(to_native(exc), commands=commands)