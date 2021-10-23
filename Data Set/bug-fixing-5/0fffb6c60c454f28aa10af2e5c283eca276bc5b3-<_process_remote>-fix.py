def _process_remote(self, host, path, user, port_matches_localhost_port):
    "\n        :arg host: hostname for the path\n        :arg path: file path\n        :arg user: username for the transfer\n        :arg port_matches_localhost_port: boolean whether the remote port\n            matches the port used by localhost's sshd.  This is used in\n            conjunction with seeing whether the host is localhost to know\n            if we need to have the module substitute the pathname or if it\n            is a different host (for instance, an ssh tunnelled port or an\n            alternative ssh port to a vagrant host.)\n        "
    transport = self._connection.transport
    if ((host not in C.LOCALHOST) or (transport != 'local')):
        if (port_matches_localhost_port and (host in C.LOCALHOST)):
            self._task.args['_substitute_controller'] = True
        return self._format_rsync_rsh_target(host, path, user)
    if ((':' not in path) and (not path.startswith('/'))):
        path = self._get_absolute_path(path=path)
    return path