def work(self):
    'worker'
    self.check_params()
    self.get_proposed()
    self.merge_interface(self.interface, self.mtu)
    self.set_jumboframe()
    self.get_existing()
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