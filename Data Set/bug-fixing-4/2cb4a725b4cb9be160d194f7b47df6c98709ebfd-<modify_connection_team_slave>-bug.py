def modify_connection_team_slave(self):
    cmd = [self.module.get_bin_path('nmcli', True)]
    cmd.append('con')
    cmd.append('mod')
    cmd.append(self.conn_name)
    cmd.append('connection.master')
    cmd.append(self.master)
    if (self.mtu is not None):
        cmd.append('802-3-ethernet.mtu')
        cmd.append(self.mtu)
    return cmd