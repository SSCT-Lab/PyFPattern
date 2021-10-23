

def _build_command(self, binary, *other_args):
    '\n        Takes a binary (ssh, scp, sftp) and optional extra arguments and returns\n        a command line as an array that can be passed to subprocess.Popen.\n        '
    self._command = []
    if self._play_context.password:
        if (not self._sshpass_available()):
            raise AnsibleError("to use the 'ssh' connection type with passwords, you must install the sshpass program")
        self.sshpass_pipe = os.pipe()
        self._command += ['sshpass', '-d{0}'.format(self.sshpass_pipe[0])]
    self._command += [binary]
    if ((binary == 'sftp') and C.DEFAULT_SFTP_BATCH_MODE):
        if self._play_context.password:
            self._add_args('disable batch mode for sshpass', ['-o', 'BatchMode=no'])
        self._command += ['-b', '-']
    self._command += ['-C']
    if (self._play_context.verbosity > 3):
        self._command += ['-vvv']
    elif (binary == 'ssh'):
        self._command += ['-q']
    if self._play_context.ssh_args:
        args = self._split_ssh_args(self._play_context.ssh_args)
        self._add_args('ansible.cfg set ssh_args', args)
    if (not C.HOST_KEY_CHECKING):
        self._add_args('ANSIBLE_HOST_KEY_CHECKING/host_key_checking disabled', ('-o', 'StrictHostKeyChecking=no'))
    if (self._play_context.port is not None):
        self._add_args('ANSIBLE_REMOTE_PORT/remote_port/ansible_port set', ('-o', 'Port={0}'.format(self._play_context.port)))
    key = self._play_context.private_key_file
    if key:
        self._add_args('ANSIBLE_PRIVATE_KEY_FILE/private_key_file/ansible_ssh_private_key_file set', ('-o', 'IdentityFile="{0}"'.format(os.path.expanduser(key))))
    if (not self._play_context.password):
        self._add_args('ansible_password/ansible_ssh_pass not set', ('-o', 'KbdInteractiveAuthentication=no', '-o', 'PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey', '-o', 'PasswordAuthentication=no'))
    user = self._play_context.remote_user
    if user:
        self._add_args('ANSIBLE_REMOTE_USER/remote_user/ansible_user/user/-u set', ('-o', 'User={0}'.format(to_bytes(self._play_context.remote_user))))
    self._add_args('ANSIBLE_TIMEOUT/timeout set', ('-o', 'ConnectTimeout={0}'.format(self._play_context.timeout)))
    for opt in ['ssh_common_args', (binary + '_extra_args')]:
        attr = getattr(self._play_context, opt, None)
        if (attr is not None):
            args = self._split_ssh_args(attr)
            self._add_args(('PlayContext set %s' % opt), args)
    (controlpersist, controlpath) = self._persistence_controls(self._command)
    if controlpersist:
        self._persistent = True
        if (not controlpath):
            cpdir = unfrackpath('$HOME/.ansible/cp')
            makedirs_safe(cpdir, 448)
            if (not os.access(cpdir, os.W_OK)):
                raise AnsibleError(('Cannot write to ControlPath %s' % cpdir))
            args = ('-o', 'ControlPath={0}'.format(to_bytes((C.ANSIBLE_SSH_CONTROL_PATH % dict(directory=cpdir)))))
            self._add_args('found only ControlPersist; added ControlPath', args)
    if other_args:
        self._command += other_args
    return self._command
