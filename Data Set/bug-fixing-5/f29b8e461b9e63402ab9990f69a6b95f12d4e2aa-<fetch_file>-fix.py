def fetch_file(self, in_path, out_path):
    ' save a remote file to the specified path '
    display.vvv(('FETCH %s TO %s' % (in_path, out_path)), host=self._play_context.remote_addr)
    data = dict(mode='fetch', in_path=in_path)
    data = jsonify(data)
    data = keyczar_encrypt(self.key, data)
    if self.send_data(data):
        raise AnsibleError(('failed to initiate the file fetch with %s' % self._play_context.remote_addr))
    fh = open(to_bytes(out_path, errors='strict'), 'w')
    try:
        bytes = 0
        while True:
            response = self.recv_data()
            if (not response):
                raise AnsibleError(('Failed to get a response from %s' % self._play_context.remote_addr))
            response = keyczar_decrypt(self.key, response)
            response = json.loads(response)
            if response.get('failed', False):
                raise AnsibleError('Error during file fetch, aborting')
            out = base64.b64decode(response['data'])
            fh.write(out)
            bytes += len(out)
            data = jsonify(dict())
            data = keyczar_encrypt(self.key, data)
            if self.send_data(data):
                raise AnsibleError('failed to send ack during file fetch')
            if response.get('last', False):
                break
    finally:
        response = self.recv_data()
        display.vvv(('FETCH wrote %d bytes to %s' % (bytes, out_path)), host=self._play_context.remote_addr)
        fh.close()