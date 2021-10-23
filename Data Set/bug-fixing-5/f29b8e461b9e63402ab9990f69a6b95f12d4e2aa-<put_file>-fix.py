def put_file(self, in_path, out_path):
    ' transfer a file from local to remote '
    display.vvv(('PUT %s TO %s' % (in_path, out_path)), host=self._play_context.remote_addr)
    in_path = to_bytes(in_path, errors='strict')
    if (not os.path.exists(in_path)):
        raise AnsibleFileNotFound(('file or module does not exist: %s' % in_path))
    fd = file(in_path, 'rb')
    fstat = os.stat(in_path)
    try:
        display.vvv(('PUT file is %d bytes' % fstat.st_size), host=self._play_context.remote_addr)
        last = False
        while ((fd.tell() <= fstat.st_size) and (not last)):
            display.vvvv(('file position currently %ld, file size is %ld' % (fd.tell(), fstat.st_size)), host=self._play_context.remote_addr)
            data = fd.read(CHUNK_SIZE)
            if (fd.tell() >= fstat.st_size):
                last = True
            data = dict(mode='put', data=base64.b64encode(data), out_path=out_path, last=last)
            if self._play_context.become:
                data['user'] = self._play_context.become_user
            data = jsonify(data)
            data = keyczar_encrypt(self.key, data)
            if self.send_data(data):
                raise AnsibleError(('failed to send the file to %s' % self._play_context.remote_addr))
            response = self.recv_data()
            if (not response):
                raise AnsibleError(('Failed to get a response from %s' % self._play_context.remote_addr))
            response = keyczar_decrypt(self.key, response)
            response = json.loads(response)
            if response.get('failed', False):
                raise AnsibleError('failed to put the file in the requested location')
    finally:
        fd.close()
        display.vvvv('waiting for final response after PUT', host=self._play_context.remote_addr)
        response = self.recv_data()
        if (not response):
            raise AnsibleError(('Failed to get a response from %s' % self._play_context.remote_addr))
        response = keyczar_decrypt(self.key, response)
        response = json.loads(response)
        if response.get('failed', False):
            raise AnsibleError('failed to put the file in the requested location')