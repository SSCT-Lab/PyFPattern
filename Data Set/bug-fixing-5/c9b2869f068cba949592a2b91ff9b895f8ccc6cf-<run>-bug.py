def run(self):
    'Returns the path of the persistent connection socket.\n\n        Attempts to ensure (within playcontext.timeout seconds) that the\n        socket path exists. If the path exists (or the timeout has expired),\n        returns the socket path.\n        '
    (p, out, err) = self._do_it('RUN:')
    while True:
        out = out.strip()
        if (out == b''):
            return None
        elif out.startswith(b'#SOCKET_PATH#'):
            break
        else:
            out = p.stdout.readline()
    socket_path = out.split(b'#SOCKET_PATH#: ', 1)[1]
    return to_text(socket_path, errors='surrogate_or_strict')