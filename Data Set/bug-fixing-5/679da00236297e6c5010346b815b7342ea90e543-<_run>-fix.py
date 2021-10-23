def _run(self, cmd, in_data, sudoable=True, checkrc=True):
    '\n        Starts the command and communicates with it until it ends.\n        '
    display_cmd = list(map(pipes.quote, map(to_text, cmd)))
    display.vvv('SSH: EXEC {0}'.format(' '.join(display_cmd)), host=self.host)
    p = None
    if isinstance(cmd, (text_type, binary_type)):
        cmd = to_bytes(cmd)
    else:
        cmd = list(map(to_bytes, cmd))
    if (not in_data):
        try:
            (master, slave) = pty.openpty()
            if (PY3 and self._play_context.password):
                p = subprocess.Popen(cmd, stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE, pass_fds=self.sshpass_pipe)
            else:
                p = subprocess.Popen(cmd, stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdin = os.fdopen(master, 'wb', 0)
            os.close(slave)
        except (OSError, IOError):
            p = None
    if (not p):
        if (PY3 and self._play_context.password):
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, pass_fds=self.sshpass_pipe)
        else:
            p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdin = p.stdin
    if self._play_context.password:
        os.close(self.sshpass_pipe[0])
        try:
            os.write(self.sshpass_pipe[1], (to_bytes(self._play_context.password) + b'\n'))
        except OSError as e:
            if ((e.errno != errno.EPIPE) or (p.poll() is None)):
                raise
        os.close(self.sshpass_pipe[1])
    states = ['awaiting_prompt', 'awaiting_escalation', 'ready_to_send', 'awaiting_exit']
    state = states.index('ready_to_send')
    if (b'ssh' in cmd):
        if self._play_context.prompt:
            state = states.index('awaiting_prompt')
            display.debug(('Initial state: %s: %s' % (states[state], self._play_context.prompt)))
        elif (self._play_context.become and self._play_context.success_key):
            state = states.index('awaiting_escalation')
            display.debug(('Initial state: %s: %s' % (states[state], self._play_context.success_key)))
    b_stdout = b_stderr = b''
    b_tmp_stdout = b_tmp_stderr = b''
    self._flags = dict(become_prompt=False, become_success=False, become_error=False, become_nopasswd_error=False)
    timeout = (2 + self._play_context.timeout)
    rpipes = [p.stdout, p.stderr]
    for fd in rpipes:
        fcntl.fcntl(fd, fcntl.F_SETFL, (fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK))
    if ((states[state] == 'ready_to_send') and in_data):
        self._send_initial_data(stdin, in_data)
        state += 1
    while True:
        (rfd, wfd, efd) = select.select(rpipes, [], [], timeout)
        if (not rfd):
            if (state <= states.index('awaiting_escalation')):
                if (p.poll() is not None):
                    break
                self._terminate_process(p)
                raise AnsibleError(('Timeout (%ds) waiting for privilege escalation prompt: %s' % (timeout, to_native(b_stdout))))
        if (p.stdout in rfd):
            b_chunk = p.stdout.read()
            if (b_chunk == b''):
                rpipes.remove(p.stdout)
                timeout = 1
            b_tmp_stdout += b_chunk
            display.debug(('stdout chunk (state=%s):\n>>>%s<<<\n' % (state, to_text(b_chunk))))
        if (p.stderr in rfd):
            b_chunk = p.stderr.read()
            if (b_chunk == b''):
                rpipes.remove(p.stderr)
            b_tmp_stderr += b_chunk
            display.debug(('stderr chunk (state=%s):\n>>>%s<<<\n' % (state, to_text(b_chunk))))
        if (state < states.index('ready_to_send')):
            if b_tmp_stdout:
                (b_output, b_unprocessed) = self._examine_output('stdout', states[state], b_tmp_stdout, sudoable)
                b_stdout += b_output
                b_tmp_stdout = b_unprocessed
            if b_tmp_stderr:
                (b_output, b_unprocessed) = self._examine_output('stderr', states[state], b_tmp_stderr, sudoable)
                b_stderr += b_output
                b_tmp_stderr = b_unprocessed
        else:
            b_stdout += b_tmp_stdout
            b_stderr += b_tmp_stderr
            b_tmp_stdout = b_tmp_stderr = b''
        if (states[state] == 'awaiting_prompt'):
            if self._flags['become_prompt']:
                display.debug('Sending become_pass in response to prompt')
                stdin.write((to_bytes(self._play_context.become_pass) + b'\n'))
                self._flags['become_prompt'] = False
                state += 1
            elif self._flags['become_success']:
                state += 1
        if (states[state] == 'awaiting_escalation'):
            if self._flags['become_success']:
                display.debug('Escalation succeeded')
                self._flags['become_success'] = False
                state += 1
            elif self._flags['become_error']:
                display.debug('Escalation failed')
                self._terminate_process(p)
                self._flags['become_error'] = False
                raise AnsibleError(('Incorrect %s password' % self._play_context.become_method))
            elif self._flags['become_nopasswd_error']:
                display.debug('Escalation requires password')
                self._terminate_process(p)
                self._flags['become_nopasswd_error'] = False
                raise AnsibleError(('Missing %s password' % self._play_context.become_method))
            elif self._flags['become_prompt']:
                display.debug('Escalation prompt repeated')
                self._terminate_process(p)
                self._flags['become_prompt'] = False
                raise AnsibleError(('Incorrect %s password' % self._play_context.become_method))
        if (states[state] == 'ready_to_send'):
            if in_data:
                self._send_initial_data(stdin, in_data)
            state += 1
        if (p.poll() is not None):
            if ((not rpipes) or (not rfd)):
                break
            timeout = 0
            continue
        elif (not rpipes):
            p.wait()
            break
    stdin.close()
    if C.HOST_KEY_CHECKING:
        if ((cmd[0] == b'sshpass') and (p.returncode == 6)):
            raise AnsibleError("Using a SSH password instead of a key is not possible because Host Key checking is enabled and sshpass does not support this.  Please add this host's fingerprint to your known_hosts file to manage this host.")
    controlpersisterror = ((b'Bad configuration option: ControlPersist' in b_stderr) or (b'unknown configuration option: ControlPersist' in b_stderr))
    if ((p.returncode != 0) and controlpersisterror):
        raise AnsibleError('using -c ssh on certain older ssh versions may not support ControlPersist, set ANSIBLE_SSH_ARGS="" (or ssh_args in [ssh_connection] section of the config file) before running again')
    if ((p.returncode == 255) and in_data and checkrc):
        raise AnsibleConnectionFailure('SSH Error: data could not be sent to the remote host. Make sure this host can be reached over ssh')
    return (p.returncode, b_stdout, b_stderr)