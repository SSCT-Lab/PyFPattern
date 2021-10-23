def _build_command(self, binary, *other_args):
    '\n        Takes a binary (ssh, scp, sftp) and optional extra arguments and returns\n        a command line as an array that can be passed to subprocess.Popen.\n        '
    b_command = []
    if self._play_context.password:
        if (not self._sshpass_available()):
            raise AnsibleError("to use the 'ssh' connection type with passwords, you must install the sshpass program")
        self.sshpass_pipe = os.pipe()
        b_command += [b'sshpass', (b'-d' + to_bytes(self.sshpass_pipe[0], nonstring='simplerepr', errors='surrogate_or_strict'))]
    if (binary == 'ssh'):
        b_command += [to_bytes(self._play_context.ssh_executable, errors='surrogate_or_strict')]
    else:
        b_command += [to_bytes(binary, errors='surrogate_or_strict')]
    if ((binary == 'sftp') and C.DEFAULT_SFTP_BATCH_MODE):
        if self._play_context.password:
            b_args = [b'-o', b'BatchMode=no']
            self._add_args(b_command, b_args, 'disable batch mode for sshpass')
        b_command += [b'-b', b'-']
    if (self._play_context.verbosity > 3):
        b_command.append(b'-vvv')
    if self._play_context.ssh_args:
        b_args = [to_bytes(a, errors='surrogate_or_strict') for a in self._split_ssh_args(self._play_context.ssh_args)]
        self._add_args(b_command, b_args, 'ansible.cfg set ssh_args')
    if (not C.HOST_KEY_CHECKING):
        b_args = (b'-o', b'StrictHostKeyChecking=no')
        self._add_args(b_command, b_args, 'ANSIBLE_HOST_KEY_CHECKING/host_key_checking disabled')
    if (self._play_context.port is not None):
        b_args = (b'-o', (b'Port=' + to_bytes(self._play_context.port, nonstring='simplerepr', errors='surrogate_or_strict')))
        self._add_args(b_command, b_args, 'ANSIBLE_REMOTE_PORT/remote_port/ansible_port set')
    key = self._play_context.private_key_file
    if key:
        b_args = (b'-o', ((b'IdentityFile="' + to_bytes(os.path.expanduser(key), errors='surrogate_or_strict')) + b'"'))
        self._add_args(b_command, b_args, 'ANSIBLE_PRIVATE_KEY_FILE/private_key_file/ansible_ssh_private_key_file set')
    if (not self._play_context.password):
        self._add_args(b_command, (b'-o', b'KbdInteractiveAuthentication=no', b'-o', b'PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey', b'-o', b'PasswordAuthentication=no'), 'ansible_password/ansible_ssh_pass not set')
    user = self._play_context.remote_user
    if user:
        self._add_args(b_command, (b'-o', (b'User=' + to_bytes(self._play_context.remote_user, errors='surrogate_or_strict'))), 'ANSIBLE_REMOTE_USER/remote_user/ansible_user/user/-u set')
    self._add_args(b_command, (b'-o', (b'ConnectTimeout=' + to_bytes(self._play_context.timeout, errors='surrogate_or_strict', nonstring='simplerepr'))), 'ANSIBLE_TIMEOUT/timeout set')
    for opt in ('ssh_common_args', '{0}_extra_args'.format(binary)):
        attr = getattr(self._play_context, opt, None)
        if (attr is not None):
            b_args = [to_bytes(a, errors='surrogate_or_strict') for a in self._split_ssh_args(attr)]
            self._add_args(b_command, b_args, ('PlayContext set %s' % opt))
    (controlpersist, controlpath) = self._persistence_controls(b_command)
    if controlpersist:
        self._persistent = True
        if (not controlpath):
            cpdir = unfrackpath(self.control_path_dir)
            b_cpdir = to_bytes(cpdir, errors='surrogate_or_strict')
            makedirs_safe(b_cpdir, 448)
            if (not os.access(b_cpdir, os.W_OK)):
                raise AnsibleError(('Cannot write to ControlPath %s' % to_native(cpdir)))
            if (not self.control_path):
                self.control_path = self._create_control_path(self.host, self.port, self.user)
            b_args = (b'-o', (b'ControlPath=' + to_bytes((self.control_path % dict(directory=cpdir)), errors='surrogate_or_strict')))
            self._add_args(b_command, b_args, 'found only ControlPersist; added ControlPath')
    if other_args:
        b_command += [to_bytes(a) for a in other_args]
    return b_command