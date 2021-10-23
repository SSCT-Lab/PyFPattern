@_ssh_retry
def _file_transport_command(self, in_path, out_path, sftp_action):
    host = ('[%s]' % self.host)
    methods = []
    ssh_transfer_method = self._play_context.ssh_transfer_method
    if (ssh_transfer_method is not None):
        if (not (ssh_transfer_method in ('smart', 'sftp', 'scp', 'piped'))):
            raise AnsibleOptionsError('transfer_method needs to be one of [smart|sftp|scp|piped]')
        if (ssh_transfer_method == 'smart'):
            methods = ['sftp', 'scp', 'piped']
        else:
            methods = [ssh_transfer_method]
    else:
        scp_if_ssh = C.DEFAULT_SCP_IF_SSH
        if (not isinstance(scp_if_ssh, bool)):
            scp_if_ssh = scp_if_ssh.lower()
            if (scp_if_ssh in BOOLEANS):
                scp_if_ssh = boolean(scp_if_ssh, strict=False)
            elif (scp_if_ssh != 'smart'):
                raise AnsibleOptionsError('scp_if_ssh needs to be one of [smart|True|False]')
        if (scp_if_ssh == 'smart'):
            methods = ['sftp', 'scp', 'piped']
        elif (scp_if_ssh is True):
            methods = ['scp']
        else:
            methods = ['sftp']
    for method in methods:
        returncode = stdout = stderr = None
        if (method == 'sftp'):
            cmd = self._build_command('sftp', to_bytes(host))
            in_data = '{0} {1} {2}\n'.format(sftp_action, shlex_quote(in_path), shlex_quote(out_path))
            in_data = to_bytes(in_data, nonstring='passthru')
            (returncode, stdout, stderr) = self._bare_run(cmd, in_data, checkrc=False)
        elif (method == 'scp'):
            if (sftp_action == 'get'):
                cmd = self._build_command('scp', '{0}:{1}'.format(host, shlex_quote(in_path)), out_path)
            else:
                cmd = self._build_command('scp', in_path, '{0}:{1}'.format(host, shlex_quote(out_path)))
            in_data = None
            (returncode, stdout, stderr) = self._bare_run(cmd, in_data, checkrc=False)
        elif (method == 'piped'):
            if (sftp_action == 'get'):
                (returncode, stdout, stderr) = self.exec_command(('dd if=%s bs=%s' % (in_path, BUFSIZE)), sudoable=False)
                out_file = open(to_bytes(out_path, errors='surrogate_or_strict'), 'wb+')
                out_file.write(stdout)
                out_file.close()
            else:
                in_data = open(to_bytes(in_path, errors='surrogate_or_strict'), 'rb').read()
                in_data = to_bytes(in_data, nonstring='passthru')
                (returncode, stdout, stderr) = self.exec_command(('dd of=%s bs=%s' % (out_path, BUFSIZE)), in_data=in_data, sudoable=False)
        if (returncode == 0):
            return (returncode, stdout, stderr)
        elif (len(methods) > 1):
            display.warning(msg=('%s transfer mechanism failed on %s. Use ANSIBLE_DEBUG=1 to see detailed information' % (method, host)))
            display.debug(msg=('%s' % to_native(stdout)))
            display.debug(msg=('%s' % to_native(stderr)))
    if (returncode == 255):
        raise AnsibleConnectionFailure(('Failed to connect to the host via %s: %s' % (method, to_native(stderr))))
    else:
        raise AnsibleError(('failed to transfer file to %s %s:\n%s\n%s' % (to_native(in_path), to_native(out_path), to_native(stdout), to_native(stderr))))