def _new_docker_version(self):
    cmd_args = []
    if self._play_context.docker_extra_args:
        cmd_args += self._play_context.docker_extra_args.split(' ')
    new_version_subcommand = ['version', '--format', "'{{.Server.Version}}'"]
    new_docker_cmd = (([self.docker_cmd] + cmd_args) + new_version_subcommand)
    p = subprocess.Popen(new_docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (cmd_output, err) = p.communicate()
    return (new_docker_cmd, to_native(cmd_output), err, p.returncode)