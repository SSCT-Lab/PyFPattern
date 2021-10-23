def _get_docker_version(self):
    (cmd, cmd_output, err, returncode) = self._old_docker_version()
    if (returncode == 0):
        for line in to_text(cmd_output, errors='surrogate_or_strict').split('\n'):
            if line.startswith('Server version:'):
                return self._sanitize_version(line.split()[2])
    (cmd, cmd_output, err, returncode) = self._new_docker_version()
    if returncode:
        raise AnsibleError(('Docker version check (%s) failed: %s' % (to_native(cmd), to_native(err))))
    return self._sanitize_version(to_text(cmd_output, errors='surrogate_or_strict'))