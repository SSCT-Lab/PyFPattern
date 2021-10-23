def _connect(self):
    if (not self.connected):
        protocol = ('https' if self.get_option('use_ssl') else 'http')
        host = self.get_option('host')
        port = (self.get_option('port') or (443 if (protocol == 'https') else 80))
        self._url = ('%s://%s:%s' % (protocol, host, port))
        self.queue_message('vvv', ('ESTABLISH HTTP(S) CONNECTFOR USER: %s TO %s' % (self._play_context.remote_user, self._url)))
        self.httpapi.set_become(self._play_context)
        self.httpapi.login(self.get_option('remote_user'), self.get_option('password'))
        self._connected = True