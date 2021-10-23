def delete_dfs_group_attribute(self):
    'delete dfg group attribute info'
    cmd = ('dfs-group %s' % self.dfs_group_id)
    self.cli_add_command(cmd)
    change = False
    if (self.priority_id and (self.dfs_group_info['priority'] == self.priority_id)):
        cmd = ('priority %s' % self.priority_id)
        self.cli_add_command(cmd, True)
        change = True
    if (self.ip_address and (self.dfs_group_info['ipAddress'] == self.ip_address)):
        if (self.vpn_instance_name and (self.dfs_group_info['srcVpnName'] == self.vpn_instance_name)):
            cmd = ('source ip %s vpn-instance %s' % (self.ip_address, self.vpn_instance_name))
            self.cli_add_command(cmd, True)
        else:
            cmd = ('source ip %s' % self.ip_address)
            self.cli_add_command(cmd, True)
        change = True
    if (self.nickname and (self.dfs_group_info['localNickname'] == self.nickname)):
        cmd = ('source nickname %s' % self.nickname)
        self.cli_add_command(cmd, True)
        change = True
    if (self.pseudo_nickname and (self.dfs_group_info['pseudoNickname'] == self.pseudo_nickname)):
        if self.pseudo_priority:
            cmd = ('pseudo-nickname %s priority %s' % (self.pseudo_nickname, self.pseudo_priority))
            self.cli_add_command(cmd, True)
        else:
            cmd = ('pseudo-nickname %s' % self.pseudo_nickname)
            self.cli_add_command(cmd, True)
        change = True
    if change:
        self.cli_load_config(self.commands)
        self.changed = True