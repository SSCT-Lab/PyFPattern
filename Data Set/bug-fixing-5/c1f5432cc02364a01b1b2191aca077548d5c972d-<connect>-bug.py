def connect(self):
    try:
        self.omapi = Omapi(self.module.params['host'], self.module.params['port'], self.module.params['key_name'], self.module.params['key'])
    except socket.error:
        e = get_exception()
        self.module.fail_json(msg=('Unable to connect to OMAPI server: %s' % e))