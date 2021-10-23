def create_connection_bond_slave(self):
    cmd = [self.module.get_bin_path('nmcli', True)]
    cmd.append('connection')
    cmd.append('add')
    cmd.append('type')
    cmd.append('bond-slave')
    cmd.append('con-name')
    if (self.conn_name is not None):
        cmd.append(self.conn_name)
    elif (self.ifname is not None):
        cmd.append(self.ifname)
    cmd.append('ifname')
    if (self.ifname is not None):
        cmd.append(self.ifname)
    elif (self.conn_name is not None):
        cmd.append(self.conn_name)
    cmd.append('master')
    if (self.conn_name is not None):
        cmd.append(self.master)
    return cmd