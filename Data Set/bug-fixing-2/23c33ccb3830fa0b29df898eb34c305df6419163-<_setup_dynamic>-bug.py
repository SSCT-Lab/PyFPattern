

def _setup_dynamic(self):
    'Request AWS credentials through the Ansible Core CI service.'
    display.info(('Provisioning %s cloud environment.' % self.platform), verbosity=1)
    config = self._read_config_template()
    aci = self._create_ansible_core_ci()
    response = aci.start()
    if (not self.args.explain):
        credentials = response['aws']['credentials']
        values = dict(ACCESS_KEY=credentials['access_key'], SECRET_KEY=credentials['secret_key'], SECURITY_TOKEN=credentials['session_token'], REGION='us-east-1')
        config = self._populate_config_template(config, values)
    self._write_config(config)
