def _setup_static(self):
    parser = ConfigParser()
    parser.read(self.config_static_path)
    self.endpoint = parser.get('DEFAULT', 'vcenter_hostname')
    self.port = parser.get('DEFAULT', 'vcenter_port')
    if (parser.get('DEFAULT', 'vmware_validate_certs').lower() in ('no', 'false')):
        self.insecure = True
    self._wait_for_service()