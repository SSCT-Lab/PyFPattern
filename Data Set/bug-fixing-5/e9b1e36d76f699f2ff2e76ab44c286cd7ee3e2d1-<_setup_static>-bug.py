def _setup_static(self):
    parser = ConfigParser({
        'vcenter_port': '443',
        'vmware_proxy_host': None,
        'vmware_proxy_port': None,
    })
    parser.read(self.config_static_path)
    self.endpoint = parser.get('DEFAULT', 'vcenter_hostname')
    self.port = parser.get('DEFAULT', 'vcenter_port')
    if (parser.get('DEFAULT', 'vmware_validate_certs').lower() in ('no', 'false')):
        self.insecure = True
    proxy_host = parser.get('DEFAULT', 'vmware_proxy_host')
    proxy_port = int(parser.get('DEFAULT', 'vmware_proxy_port'))
    if (proxy_host and proxy_port):
        self.proxy = ('http://%s:%d' % (proxy_host, proxy_port))
    self._wait_for_service()