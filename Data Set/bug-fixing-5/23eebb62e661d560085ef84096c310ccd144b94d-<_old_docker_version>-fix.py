def _old_docker_version(self):
    cmd_args = []
    if self._play_context.docker_extra_args:
        cmd_args += self._play_context.docker_extra_args.split(' ')
    old_version_subcommand = ['version']
    old_docker_cmd = (([self.docker_cmd] + cmd_args) + old_version_subcommand)
    p = subprocess.Popen(old_docker_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (cmd_output, err) = p.communicate()
    return (old_docker_cmd, to_native(cmd_output), err, p.returncode)