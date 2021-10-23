

def exec_command(self, cmd, in_data=None, sudoable=True):
    ' run a command on the remote host '
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    if in_data:
        raise AnsibleError('Internal Error: this module does not support optimized module pipelining')
    bufsize = 4096
    try:
        self.ssh.get_transport().set_keepalive(5)
        chan = self.ssh.get_transport().open_session()
    except Exception as e:
        msg = 'Failed to open session'
        if (len(str(e)) > 0):
            msg += (': %s' % str(e))
        raise AnsibleConnectionFailure(msg)
    if (C.PARAMIKO_PTY and sudoable):
        chan.get_pty(term=os.getenv('TERM', 'vt100'), width=int(os.getenv('COLUMNS', 0)), height=int(os.getenv('LINES', 0)))
    display.vvv(('EXEC %s' % cmd), host=self._play_context.remote_addr)
    cmd = to_bytes(cmd, errors='strict')
    no_prompt_out = ''
    no_prompt_err = ''
    become_output = ''
    try:
        chan.exec_command(cmd)
        if self._play_context.prompt:
            passprompt = False
            become_sucess = False
            while (not (become_sucess or passprompt)):
                display.debug('Waiting for Privilege Escalation input')
                chunk = chan.recv(bufsize)
                display.debug(('chunk is: %s' % chunk))
                if (not chunk):
                    if ('unknown user' in become_output):
                        raise AnsibleError(('user %s does not exist' % self._play_context.become_user))
                    else:
                        break
                become_output += chunk
                for l in become_output.splitlines(True):
                    if self.check_become_success(l):
                        become_sucess = True
                        break
                    elif self.check_password_prompt(l):
                        passprompt = True
                        break
            if passprompt:
                if (self._play_context.become and self._play_context.become_pass):
                    chan.sendall((self._play_context.become_pass + '\n'))
                else:
                    raise AnsibleError('A password is reqired but none was supplied')
            else:
                no_prompt_out += become_output
                no_prompt_err += become_output
    except socket.timeout:
        raise AnsibleError(('ssh timed out waiting for privilege escalation.\n' + become_output))
    stdout = ''.join(chan.makefile('rb', bufsize))
    stderr = ''.join(chan.makefile_stderr('rb', bufsize))
    return (chan.recv_exit_status(), (no_prompt_out + stdout), (no_prompt_out + stderr))
