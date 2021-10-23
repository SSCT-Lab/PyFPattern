def modify_connection_team_slave(self):
    cmd = [self.nmcli_bin, 'con', 'mod', self.conn_name, 'connection.master', self.master]
    if (self.mtu is not None):
        cmd.append('802-3-ethernet.mtu')
        cmd.append(self.mtu)
    return cmd