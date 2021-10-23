def delete_mlag_global(self):
    'delete mlag global attribute info'
    if self.is_mlag_global_info_exist():
        if self.mlag_priority_id:
            cmd = ('lacp m-lag priority %s' % self.mlag_priority_id)
            self.cli_add_command(cmd, True)
        if self.mlag_system_id:
            cmd = ('lacp m-lag system-id %s' % self.mlag_system_id)
            self.cli_add_command(cmd, True)
        if self.commands:
            self.cli_load_config(self.commands)
            self.changed = True