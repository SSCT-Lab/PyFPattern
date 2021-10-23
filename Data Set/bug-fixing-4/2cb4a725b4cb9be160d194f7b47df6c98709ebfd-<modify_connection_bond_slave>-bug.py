def modify_connection_bond_slave(self):
    cmd = [self.module.get_bin_path('nmcli', True)]
    cmd.append('con')
    cmd.append('mod')
    cmd.append(self.conn_name)
    cmd.append('connection.master')
    cmd.append(self.master)
    return cmd