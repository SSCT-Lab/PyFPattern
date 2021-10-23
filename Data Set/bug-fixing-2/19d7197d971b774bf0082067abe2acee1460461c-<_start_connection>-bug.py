

def _start_connection(self):
    '\n        Starts the persistent connection\n        '
    candidate_paths = [(C.ANSIBLE_CONNECTION_PATH or os.path.dirname(sys.argv[0]))]
    candidate_paths.extend(os.environ['PATH'].split(os.pathsep))
    for dirname in candidate_paths:
        ansible_connection = os.path.join(dirname, 'ansible-connection')
        if os.path.isfile(ansible_connection):
            break
    else:
        raise AnsibleError("Unable to find location of 'ansible-connection'. Please set or check the value of ANSIBLE_CONNECTION_PATH")
    python = sys.executable
    (master, slave) = pty.openpty()
    p = subprocess.Popen([python, ansible_connection, to_text(os.getppid())], stdin=slave, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.close(slave)
    old = termios.tcgetattr(master)
    new = termios.tcgetattr(master)
    new[3] = (new[3] & (~ termios.ICANON))
    try:
        termios.tcsetattr(master, termios.TCSANOW, new)
        write_to_file_descriptor(master, {
            'ansible_command_timeout': self.get_option('persistent_command_timeout'),
        })
        write_to_file_descriptor(master, self._play_context.serialize())
        (stdout, stderr) = p.communicate()
    finally:
        termios.tcsetattr(master, termios.TCSANOW, old)
    os.close(master)
    if (p.returncode == 0):
        result = json.loads(to_text(stdout, errors='surrogate_then_replace'))
    else:
        try:
            result = json.loads(to_text(stderr, errors='surrogate_then_replace'))
        except getattr(json.decoder, 'JSONDecodeError', ValueError):
            result = {
                'error': to_text(stderr, errors='surrogate_then_replace'),
            }
    if ('messages' in result):
        for msg in result.get('messages'):
            display.vvvv(('%s' % msg), host=self._play_context.remote_addr)
    if ('error' in result):
        if (self._play_context.verbosity > 2):
            if result.get('exception'):
                msg = ('The full traceback is:\n' + result['exception'])
                display.display(msg, color=C.COLOR_ERROR)
        raise AnsibleError(result['error'])
    return result['socket_path']
