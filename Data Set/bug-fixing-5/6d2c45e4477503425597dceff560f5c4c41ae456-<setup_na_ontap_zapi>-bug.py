def setup_na_ontap_zapi(module, vserver=None):
    hostname = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    https = module.params['https']
    validate_certs = module.params['validate_certs']
    port = module.params['http_port']
    if HAS_NETAPP_LIB:
        server = zapi.NaServer(hostname)
        server.set_username(username)
        server.set_password(password)
        if vserver:
            server.set_vserver(vserver)
        server.set_api_version(major=1, minor=110)
        if https:
            if (port is None):
                port = 443
            transport_type = 'HTTPS'
            if (validate_certs is True):
                if ((not os.environ.get('PYTHONHTTPSVERIFY', '')) and getattr(ssl, '_create_unverified_context', None)):
                    ssl._create_default_https_context = ssl._create_unverified_context
        else:
            if (port is None):
                port = 80
            transport_type = 'HTTP'
        server.set_transport_type(transport_type)
        server.set_port(port)
        server.set_server_type('FILER')
        return server
    else:
        module.fail_json(msg='the python NetApp-Lib module is required')