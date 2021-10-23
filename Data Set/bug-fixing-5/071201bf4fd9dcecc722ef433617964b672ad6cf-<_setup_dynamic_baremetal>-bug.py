def _setup_dynamic_baremetal(self):
    'Request Esxi credentials through the Ansible Core CI service.'
    display.info(('Provisioning %s cloud environment.' % self.platform), verbosity=1)
    config = self._read_config_template()
    aci = self._create_ansible_core_ci()
    if (not self.args.explain):
        self.aci = aci
        aci.start()
        aci.wait(iterations=160)
        data = aci.get().response_json.get('data')
        config = self._populate_config_template(config, data)
        self._write_config(config)