def delete_mlag_interface(self):
    'delete mlag interface attribute info'
    if self.is_mlag_interface_info_exist():
        mlag_port = 'Eth-Trunk'
        mlag_port += self.eth_trunk_id
        cmd = ('interface %s' % mlag_port)
        self.cli_add_command(cmd)
        if self.mlag_priority_id:
            cmd = ('lacp m-lag priority %s' % self.mlag_priority_id)
            self.cli_add_command(cmd, True)
        if self.mlag_system_id:
            cmd = ('lacp m-lag system-id %s' % self.mlag_system_id)
            self.cli_add_command(cmd, True)
        if self.commands:
            self.cli_load_config(self.commands)
            self.changed = True