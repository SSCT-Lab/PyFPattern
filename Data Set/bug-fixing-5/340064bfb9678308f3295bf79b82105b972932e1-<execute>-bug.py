def execute(self, cmd, timeout=200, capture_output=True):
    "\n        Executes a HAProxy command by sending a message to a HAProxy's local\n        UNIX socket and waiting up to 'timeout' milliseconds for the response.\n        "
    self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.client.connect(self.socket)
    self.client.sendall(('%s\n' % cmd))
    result = ''
    buf = ''
    buf = self.client.recv(RECV_SIZE)
    while buf:
        result += buf
        buf = self.client.recv(RECV_SIZE)
    if capture_output:
        self.capture_command_output(cmd, result.strip())
    self.client.close()
    return result