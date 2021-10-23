def get_instances(self):
    ' Get a list of vm instances with pyvmomi '
    kwargs = {
        'host': self.server,
        'user': self.username,
        'pwd': self.password,
        'port': int(self.port),
    }
    if (self.validate_certs and hasattr(ssl, 'SSLContext')):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        kwargs['sslContext'] = context
    elif (self.validate_certs and (not hasattr(ssl, 'SSLContext'))):
        sys.exit('pyVim does not support changing verification mode with python < 2.7.9. Either update python or use validate_certs=false.')
    elif ((not self.validate_certs) and hasattr(ssl, 'SSLContext')):
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_NONE
        context.check_hostname = False
        kwargs['sslContext'] = context
    elif ((not self.validate_certs) and (not hasattr(ssl, 'SSLContext'))):
        pass
    return self._get_instances(kwargs)