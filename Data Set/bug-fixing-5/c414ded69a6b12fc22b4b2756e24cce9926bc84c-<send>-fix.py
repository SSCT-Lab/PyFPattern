def send(self, obj):
    try:
        command = obj['command']
        self._history.append(command)
        self._shell.sendall(('%s\r' % command))
        return self.receive(obj)
    except (socket.timeout, AttributeError):
        raise AnsibleConnectionFailure(('timeout trying to send command: %s' % command.strip()))