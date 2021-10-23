def modify_connection_bond_slave(self):
    cmd = [self.nmcli_bin, 'con', 'mod', self.conn_name, 'connection.master', self.master]
    return cmd