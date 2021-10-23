def send(self, obj):
    'Sends the command to the device in the opened shell'
    try:
        command = obj['command']
        self._history.append(command)
        self._shell.sendall(('%s\r' % command))
        return self.receive(obj)
    except (socket.timeout, AttributeError):
        raise AnsibleConnectionFailure(('timeout trying to send command: %s' % command.strip()))