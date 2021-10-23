def work(self):
    'worker'
    self.check_params()
    self.get_existing()
    self.get_proposed()
    if self.dfs_group_id:
        if (self.state == 'present'):
            if self.dfs_group_info:
                if (self.nickname or self.pseudo_nickname or self.pseudo_priority or self.priority_id or self.ip_address or self.vpn_instance_name):
                    if self.nickname:
                        if (self.dfs_group_info['ipAddress'] not in ['0.0.0.0', None]):
                            self.module.fail_json(msg='Error: nickname and ip_address can not be exist at the same time.')
                    if self.ip_address:
                        if (self.dfs_group_info['localNickname'] not in ['0', None]):
                            self.module.fail_json(msg='Error: nickname and ip_address can not be exist at the same time.')
                    self.modify_dfs_group()
            else:
                self.create_dfs_group()
        else:
            if (not self.dfs_group_info):
                self.module.fail_json(msg='Error: DFS Group does not exist.')
            if ((not self.nickname) and (not self.pseudo_nickname) and (not self.pseudo_priority) and (not self.priority_id) and (not self.ip_address) and (not self.vpn_instance_name)):
                self.delete_dfs_group()
            else:
                self.updates_cmd.append('dfs-group 1')
                self.delete_dfs_group_attribute()
                self.delete_dfs_group_nick()
                if ('undo dfs-group 1' in self.updates_cmd):
                    self.updates_cmd = ['undo dfs-group 1']
    if (self.eth_trunk_id and (not self.peer_link_id)):
        self.module.fail_json(msg='Error: eth_trunk_id and peer_link_id must be config at the same time.')
    if (self.peer_link_id and (not self.eth_trunk_id)):
        self.module.fail_json(msg='Error: eth_trunk_id and peer_link_id must be config at the same time.')
    if (self.eth_trunk_id and self.peer_link_id):
        if (self.state == 'present'):
            self.modify_peer_link()
        elif self.peer_link_info:
            self.delete_peer_link()
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