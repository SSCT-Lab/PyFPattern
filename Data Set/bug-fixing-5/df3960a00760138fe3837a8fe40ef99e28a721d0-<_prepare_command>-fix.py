def _prepare_command(self, cmd):
    connection_cmd = ['ssh', self._host_ref(), '-o', 'ControlMaster=no']
    if self.sshpass:
        connection_cmd = (['sshpass', '-e'] + connection_cmd)
    else:
        connection_cmd += ['-o', 'BatchMode=yes']
    if self.conn.port:
        connection_cmd += ['-p', str(self.conn.port)]
    if self.connect_timeout:
        connection_cmd += ['-o', 'ConnectionTimeout={}'.format(self.connect_timeout)]
    if self.no_host_key_check:
        connection_cmd += ['-o', 'UserKnownHostsFile=/dev/null', '-o', 'StrictHostKeyChecking=no']
    if self.key_file:
        connection_cmd += ['-i', self.key_file]
    if self.tty:
        connection_cmd += ['-t']
    connection_cmd += cmd
    logging.debug('SSH cmd: {} '.format(connection_cmd))
    return connection_cmd