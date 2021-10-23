def _run(self, cmd, in_data, sudoable=True):
    '\n        Starts the command and communicates with it until it ends.\n        '
    display_cmd = map(to_unicode, map(pipes.quote, cmd))
    display.vvv('SSH: EXEC {0}'.format(' '.join(display_cmd)), host=self.host)
    p = None
    if isinstance(cmd, (text_type, binary_type)):
        cmd = to_bytes(cmd)
    else:
        cmd = list(map(to_bytes, cmd))
    if (not in_data):
        try:
            (master, slave) = pty.openpty()
            p = subprocess.Popen(cmd, stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdin = os.fdopen(master, 'w', 0)
            os.close(slave)
        except (OSError, IOError):
            p = None
    if (not p):
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdin = p.stdin
    if self._play_context.password:
        os.close(self.sshpass_pipe[0])
        os.write(self.sshpass_pipe[1], '{0}\n'.format(to_bytes(self._play_context.password)))
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
    stdout = stderr = ''
    tmp_stdout = tmp_stderr = ''
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
                raise AnsibleError(('Timeout (%ds) waiting for privilege escalation prompt: %s' % (timeout, stdout)))
        if (p.stdout in rfd):
            chunk = p.stdout.read()
            if (chunk == ''):
                rpipes.remove(p.stdout)
            tmp_stdout += chunk
            display.debug(('stdout chunk (state=%s):\n>>>%s<<<\n' % (state, chunk)))
        if (p.stderr in rfd):
            chunk = p.stderr.read()
            if (chunk == ''):
                rpipes.remove(p.stderr)
            tmp_stderr += chunk
            display.debug(('stderr chunk (state=%s):\n>>>%s<<<\n' % (state, chunk)))
        if (state < states.index('ready_to_send')):
            if tmp_stdout:
                (output, unprocessed) = self._examine_output('stdout', states[state], tmp_stdout, sudoable)
                stdout += output
                tmp_stdout = unprocessed
            if tmp_stderr:
                (output, unprocessed) = self._examine_output('stderr', states[state], tmp_stderr, sudoable)
                stderr += output
                tmp_stderr = unprocessed
        else:
            stdout += tmp_stdout
            stderr += tmp_stderr
            tmp_stdout = tmp_stderr = ''
        if (states[state] == 'awaiting_prompt'):
            if self._flags['become_prompt']:
                display.debug('Sending become_pass in response to prompt')
                stdin.write('{0}\n'.format(to_bytes(self._play_context.become_pass)))
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
            if (p.stdout not in rpipes):
                timeout = 0
                continue
        elif (not rpipes):
            p.wait()
            break
    stdin.close()
    if C.HOST_KEY_CHECKING:
        if ((cmd[0] == b'sshpass') and (p.returncode == 6)):
            raise AnsibleError("Using a SSH password instead of a key is not possible because Host Key checking is enabled and sshpass does not support this.  Please add this host's fingerprint to your known_hosts file to manage this host.")
    controlpersisterror = (('Bad configuration option: ControlPersist' in stderr) or ('unknown configuration option: ControlPersist' in stderr))
    if ((p.returncode != 0) and controlpersisterror):
        raise AnsibleError('using -c ssh on certain older ssh versions may not support ControlPersist, set ANSIBLE_SSH_ARGS="" (or ssh_args in [ssh_connection] section of the config file) before running again')
    if ((p.returncode == 255) and in_data):
        raise AnsibleConnectionFailure('SSH Error: data could not be sent to the remote host. Make sure this host can be reached over ssh')
    return (p.returncode, stdout, stderr)