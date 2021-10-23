def get_instances(self):
    ' Get a list of vm instances with pyvmomi '
    instances = []
    kwargs = {
        'host': self.server,
        'user': self.username,
        'pwd': self.password,
        'port': int(self.port),
    }
    if hasattr(ssl, 'SSLContext'):
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        context.verify_mode = ssl.CERT_NONE
        kwargs['sslContext'] = context
    instances = self._get_instances(kwargs)
    self.debugl('### INSTANCES RETRIEVED')
    return instances