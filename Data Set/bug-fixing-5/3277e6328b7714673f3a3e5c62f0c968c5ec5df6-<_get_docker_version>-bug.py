def _get_docker_version(self):
    (cmd, cmd_output, err, returncode) = self._old_docker_version()
    if (returncode == 0):
        for line in cmd_output.split('\n'):
            if line.startswith('Server version:'):
                return self._sanitize_version(line.split()[2])
    (cmd, cmd_output, err, returncode) = self._new_docker_version()
    if returncode:
        raise AnsibleError(('Docker version check (%s) failed: %s' % (cmd, err)))
    return self._sanitize_version(cmd_output)