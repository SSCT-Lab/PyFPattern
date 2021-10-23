def remove_connection(self):
    cmd = [self.nmcli_bin, 'con', 'del', self.conn_name]
    return self.execute_command(cmd)