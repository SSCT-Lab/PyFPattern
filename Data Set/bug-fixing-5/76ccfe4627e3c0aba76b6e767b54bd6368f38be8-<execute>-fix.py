def execute(self, commands):
    try:
        for (index, item) in enumerate(commands):
            commands[index] = to_command(item)
        return self.shell.send(commands)
    except ShellError:
        exc = get_exception()
        commands = [str(c) for c in commands]
        raise NetworkError(to_native(exc), commands=commands)