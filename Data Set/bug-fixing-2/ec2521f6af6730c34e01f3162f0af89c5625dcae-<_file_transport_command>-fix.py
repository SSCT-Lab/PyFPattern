

def _file_transport_command(self, in_path, out_path, sftp_action):
    host = ('[%s]' % self.host)
    scp_if_ssh = C.DEFAULT_SCP_IF_SSH
    if (not isinstance(scp_if_ssh, bool)):
        scp_if_ssh = scp_if_ssh.lower()
        if (scp_if_ssh in BOOLEANS):
            scp_if_ssh = boolean(scp_if_ssh)
        elif (scp_if_ssh != 'smart'):
            raise AnsibleOptionsError('scp_if_ssh needs to be one of [smart|True|False]')
    methods = ['sftp']
    if (scp_if_ssh == 'smart'):
        methods.append('scp')
    elif scp_if_ssh:
        methods = ['scp']
    success = False
    res = None
    for method in methods:
        if (method == 'sftp'):
            cmd = self._build_command('sftp', to_bytes(host))
            in_data = '{0} {1} {2}\n'.format(sftp_action, shlex_quote(in_path), shlex_quote(out_path))
        elif (method == 'scp'):
            if (sftp_action == 'get'):
                cmd = self._build_command('scp', '{0}:{1}'.format(host, shlex_quote(out_path)), in_path)
            else:
                cmd = self._build_command('scp', in_path, '{0}:{1}'.format(host, shlex_quote(out_path)))
            in_data = None
        in_data = to_bytes(in_data, nonstring='passthru')
        (returncode, stdout, stderr) = self._run(cmd, in_data, checkrc=False)
        if (returncode == 0):
            success = True
            break
        else:
            if (scp_if_ssh == 'smart'):
                display.warning(msg=('%s transfer mechanism failed on %s. Use ANSIBLE_DEBUG=1 to see detailed information' % (method, host)))
                display.debug(msg=('%s' % to_native(stdout)))
                display.debug(msg=('%s' % to_native(stderr)))
            res = (returncode, stdout, stderr)
    if (not success):
        raise AnsibleError('failed to transfer file to {0}:\n{1}\n{2}'.format(to_native(out_path), to_native(res[1]), to_native(res[2])))
