def exec_command(self, cmd, in_data=None, sudoable=True):
    ' run a command on the local host '
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    display.debug('in local.exec_command()')
    executable = (C.DEFAULT_EXECUTABLE.split()[0] if C.DEFAULT_EXECUTABLE else None)
    display.vvv('EXEC {0}'.format(to_text(cmd)), host=self._play_context.remote_addr)
    display.debug('opening command with Popen()')
    if isinstance(cmd, (text_type, binary_type)):
        cmd = to_bytes(cmd)
    else:
        cmd = map(to_bytes, cmd)
    p = subprocess.Popen(cmd, shell=isinstance(cmd, (text_type, binary_type)), executable=executable, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    display.debug('done running command with Popen()')
    if (self._play_context.prompt and sudoable):
        fcntl.fcntl(p.stdout, fcntl.F_SETFL, (fcntl.fcntl(p.stdout, fcntl.F_GETFL) | os.O_NONBLOCK))
        fcntl.fcntl(p.stderr, fcntl.F_SETFL, (fcntl.fcntl(p.stderr, fcntl.F_GETFL) | os.O_NONBLOCK))
        selector = selectors.DefaultSelector()
        selector.register(p.stdout, selectors.EVENT_READ)
        selector.register(p.stderr, selectors.EVENT_READ)
        become_output = b''
        try:
            while ((not self.check_become_success(become_output)) and (not self.check_password_prompt(become_output))):
                events = selector.select(self._play_context.timeout)
                if (not events):
                    (stdout, stderr) = p.communicate()
                    raise AnsibleError(('timeout waiting for privilege escalation password prompt:\n' + to_native(become_output)))
                for (key, event) in events:
                    if (key.fileobj == p.stdout):
                        chunk = p.stdout.read()
                    elif (key.fileobj == p.stderr):
                        chunk = p.stderr.read()
                if (not chunk):
                    (stdout, stderr) = p.communicate()
                    raise AnsibleError(('privilege output closed while waiting for password prompt:\n' + to_native(become_output)))
                become_output += chunk
        finally:
            selector.close()
        if (not self.check_become_success(become_output)):
            p.stdin.write((to_bytes(self._play_context.become_pass, errors='surrogate_or_strict') + b'\n'))
        fcntl.fcntl(p.stdout, fcntl.F_SETFL, (fcntl.fcntl(p.stdout, fcntl.F_GETFL) & (~ os.O_NONBLOCK)))
        fcntl.fcntl(p.stderr, fcntl.F_SETFL, (fcntl.fcntl(p.stderr, fcntl.F_GETFL) & (~ os.O_NONBLOCK)))
    display.debug('getting output with communicate()')
    (stdout, stderr) = p.communicate(in_data)
    display.debug('done communicating')
    display.debug('done with local.exec_command()')
    return (p.returncode, stdout, stderr)