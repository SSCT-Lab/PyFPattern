def send(self, obj):
    try:
        self._history.append(str(obj['command']))
        cmd = ('%s\r' % str(obj['command']))
        self.shell.sendall(cmd)
        if obj.get('sendonly'):
            return
        signal.alarm(self._timeout)
        out = self.receive(obj)
        signal.alarm(0)
        return (0, out, '')
    except ShellError:
        exc = get_exception()
        return (1, '', to_native(exc))