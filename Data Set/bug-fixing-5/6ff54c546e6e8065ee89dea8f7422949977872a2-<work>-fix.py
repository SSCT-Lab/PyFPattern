def work(self):
    'worker'
    self.check_params()
    self.get_proposed()
    self.startup_info = self.get_startup_dict()
    self.get_existing()
    startup_info = self.startup_info['StartupInfos'][0]
    if self.cfg_file:
        if (self.cfg_file != startup_info['nextStartupFile']):
            self.startup_next_cfg_file()
    if self.software_file:
        if (self.software_file != startup_info['nextSysSoft']):
            self.startup_next_software_file()
    if self.patch_file:
        if (self.patch_file != startup_info['nextPatchFile']):
            self.startup_next_pat_file()
    if (self.action == 'display'):
        self.startup_info = self.get_startup_dict()
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