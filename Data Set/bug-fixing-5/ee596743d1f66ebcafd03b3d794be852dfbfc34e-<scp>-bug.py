def scp(self, src, dst):
    '\n        :type src: str\n        :type dst: str\n        '
    run_command(self.core_ci.args, ((['scp'] + self.ssh_args) + ['-P', str(self.core_ci.connection.port), '-q', '-r', src, dst]))