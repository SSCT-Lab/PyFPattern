def receive(self, cmd=None):
    recv = BytesIO()
    handled = False
    while True:
        data = self.shell.recv(200)
        recv.write(data)
        recv.seek((recv.tell() - len(data)))
        window = self.strip(recv.read().decode('utf8'))
        if cmd:
            if (('prompt' in cmd) and (not handled)):
                handled = self.handle_prompt(window, cmd)
        try:
            if self.find_prompt(window):
                resp = self.strip(recv.getvalue().decode('utf8'))
                if cmd:
                    resp = self.sanitize(cmd, resp)
                return resp
        except ShellError:
            exc = get_exception()
            exc.command = cmd['command']
            raise