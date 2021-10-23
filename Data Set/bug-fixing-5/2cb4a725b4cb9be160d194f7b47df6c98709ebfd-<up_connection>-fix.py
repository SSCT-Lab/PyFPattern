def up_connection(self):
    cmd = [self.nmcli_bin, 'con', 'up', self.conn_name]
    return self.execute_command(cmd)