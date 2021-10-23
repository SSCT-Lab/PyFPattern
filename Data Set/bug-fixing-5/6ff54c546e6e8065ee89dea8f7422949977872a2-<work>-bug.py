def work(self):
    'worker'
    self.check_params()
    self.get_proposed()
    self.startup_info = self.get_startup_dict()
    self.get_existing()
    if self.cfg_file:
        self.startup_next_cfg_file()
    if self.software_file:
        self.startup_next_software_file()
    if self.patch_file:
        self.startup_next_pat_file()
    if (self.action == 'display'):
        self.startup_info = self.get_startup_dict()
    self.get_end_state()
    self.results['changed'] = self.changed
    self.results['proposed'] = self.proposed
    self.results['existing'] = self.existing
    self.results['end_state'] = self.end_state
    if self.changed:
        self.results['updates'] = self.updates_cmd
    else:
        self.results['updates'] = list()
    self.module.exit_json(**self.results)