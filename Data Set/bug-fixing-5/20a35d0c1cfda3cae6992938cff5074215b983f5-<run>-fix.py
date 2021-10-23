def run(self):
    'Returns the path of the persistent connection socket.\n\n        Attempts to ensure (within playcontext.timeout seconds) that the\n        socket path exists. If the path exists (or the timeout has expired),\n        returns the socket path.\n        '
    socket_path = None
    (rc, out, err) = self._do_it('RUN:')
    match = re.search(b'#SOCKET_PATH#: (\\S+)', out)
    if match:
        socket_path = to_text(match.group(1).strip(), errors='surrogate_or_strict')
    return socket_path