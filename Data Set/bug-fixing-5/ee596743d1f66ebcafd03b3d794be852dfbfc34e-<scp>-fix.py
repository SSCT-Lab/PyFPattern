def scp(self, src, dst):
    '\n        :type src: str\n        :type dst: str\n        '
    for dummy in range(1, 3):
        try:
            run_command(self.core_ci.args, ((['scp'] + self.ssh_args) + ['-P', str(self.core_ci.connection.port), '-q', '-r', src, dst]))
            return
        except SubprocessError:
            time.sleep(10)
    raise ApplicationError(('Failed transfer: %s -> %s' % (src, dst)))