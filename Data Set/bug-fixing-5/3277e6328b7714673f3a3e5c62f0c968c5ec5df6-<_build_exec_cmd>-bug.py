def _build_exec_cmd(self, cmd):
    ' Build the local docker exec command to run cmd on remote_host\n\n            If remote_user is available and is supported by the docker\n            version we are using, it will be provided to docker exec.\n        '
    local_cmd = [self.docker_cmd]
    if self._play_context.docker_extra_args:
        local_cmd += self._play_context.docker_extra_args.split(' ')
    local_cmd += ['exec']
    if (self.remote_user is not None):
        local_cmd += ['-u', self.remote_user]
    local_cmd += (['-i', self._play_context.remote_addr] + cmd)
    return local_cmd