def get_instances(self):
    ' Get a list of vm instances with pyvmomi '
    kwargs = {
        'host': self.server,
        'user': self.username,
        'pwd': self.password,
        'port': int(self.port),
    }
    if (hasattr(ssl, 'SSLContext') and (not self.validate_certs)):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        kwargs['sslContext'] = context
    return self._get_instances(kwargs)