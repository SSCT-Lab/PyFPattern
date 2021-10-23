def load_configuration(self):
    if (not os.path.isfile(self.src)):
        self.module.fail_json(msg='Source file {} does not exist'.format(self.src))
    url = self.host.configManager.firmwareSystem.QueryFirmwareConfigUploadURL()
    url = url.replace('*', self.hostname)
    try:
        request = open_url(url=url, method='HEAD', validate_certs=self.validate_certs)
    except HTTPError as e:
        url = e.geturl()
    try:
        with open(self.src, 'rb') as file:
            data = file.read()
        request = open_url(url=url, data=data, method='PUT', validate_certs=self.validate_certs, url_username=self.username, url_password=self.password, force_basic_auth=True)
    except Exception as e:
        self.module.fail_json(msg=to_native(e))
    if (not self.host.runtime.inMaintenanceMode):
        self.enter_maintenance()
    try:
        self.host.configManager.firmwareSystem.RestoreFirmwareConfiguration(force=True)
        self.module.exit_json(changed=True)
    except Exception as e:
        self.exit_maintenance()
        self.module.fail_json(msg=to_native(e))