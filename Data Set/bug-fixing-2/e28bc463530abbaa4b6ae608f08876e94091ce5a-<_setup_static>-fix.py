

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
    self._wait_for_service()
