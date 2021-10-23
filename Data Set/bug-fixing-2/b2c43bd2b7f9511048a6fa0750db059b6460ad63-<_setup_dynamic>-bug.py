

def _setup_dynamic(self):
    'Request Tower credentials through the Ansible Core CI service.'
    display.info(('Provisioning %s cloud environment.' % self.platform), verbosity=1)
    self.version = os.environ.get('TOWER_VERSION', '3.2.3')
    self.check_tower_version(os.environ.get('TOWER_CLI_VERSION'))
    aci = get_tower_aci(self.args, self.version)
    aci.start()
    connection = aci.get()
    config = self._read_config_template()
    if (not self.args.explain):
        self.aci = aci
        values = dict(VERSION=self.version, HOST=connection.hostname, USERNAME=connection.username, PASSWORD=connection.password)
        config = self._populate_config_template(config, values)
    self._write_config(config)
