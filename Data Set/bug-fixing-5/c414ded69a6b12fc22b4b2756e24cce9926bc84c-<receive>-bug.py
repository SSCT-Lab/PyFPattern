def receive(self, obj=None):
    'Handles receiving of output from command'
    recv = StringIO()
    handled = False
    self._matched_prompt = None
    while True:
        data = self._shell.recv(256)
        recv.write(data)
        offset = ((recv.tell() - 256) if (recv.tell() > 256) else 0)
        recv.seek(offset)
        window = self._strip(recv.read())
        if (obj and (obj.get('prompt') and (not handled))):
            handled = self._handle_prompt(window, obj)
        if self._find_prompt(window):
            self._last_response = recv.getvalue()
            resp = self._strip(self._last_response)
            return self._sanitize(resp, obj)