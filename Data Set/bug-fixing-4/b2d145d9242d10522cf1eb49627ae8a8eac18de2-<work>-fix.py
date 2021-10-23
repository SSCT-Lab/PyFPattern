def work(self):
    'worker'
    self.check_params()
    self.get_proposed()
    self.get_existing()
    if (self.eth_trunk_id or self.dfs_group_id or self.mlag_id):
        self.mlag_info = self.get_mlag_info()
        if (self.eth_trunk_id and self.dfs_group_id and self.mlag_id):
            if (self.state == 'present'):
                self.create_mlag()
            else:
                self.delete_mlag()
        elif ((not self.mlag_system_id) and (not self.mlag_priority_id)):
            self.module.fail_json(msg='Error: eth_trunk_id, dfs_group_id, mlag_id must be config at the same time.')
    if (self.mlag_system_id or self.mlag_priority_id):
        if self.eth_trunk_id:
            self.mlag_trunk_attribute_info = self.get_mlag_trunk_attribute_info()
            if (self.mlag_system_id or self.mlag_priority_id):
                if (self.state == 'present'):
                    self.set_mlag_interface()
                else:
                    self.delete_mlag_interface()
        else:
            self.mlag_global_info = self.get_mlag_global_info()
            if (self.mlag_system_id or self.mlag_priority_id):
                if (self.state == 'present'):
                    self.set_mlag_global()
                else:
                    self.delete_mlag_global()
    if (self.interface or self.mlag_error_down):
        self.mlag_error_down_info = self.get_mlag_error_down_info()
        if (self.interface and self.mlag_error_down):
            if (self.mlag_error_down == 'enable'):
                self.create_mlag_error_down()
            else:
                self.delete_mlag_error_down()
        else:
            self.module.fail_json(msg='Error: interface, mlag_error_down must be config at the same time.')
    self.get_end_state()
    if (self.existing == self.end_state):
        self.changed = False
    self.results['changed'] = self.changed
    self.results['proposed'] = self.proposed
    self.results['existing'] = self.existing
    self.results['end_state'] = self.end_state
    if self.changed:
        self.results['updates'] = self.updates_cmd
    else:
        self.results['updates'] = list()
    self.module.exit_json(**self.results)