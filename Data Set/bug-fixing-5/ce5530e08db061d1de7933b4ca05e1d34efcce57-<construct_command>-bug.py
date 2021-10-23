def construct_command(self):
    uname_result = self._low_level_execute_command('uname')
    distribution = uname_result['stdout'].strip().lower()
    shutdown_command = self.SHUTDOWN_COMMANDS.get(distribution, self.SHUTDOWN_COMMAND_ARGS['linux'])
    shutdown_command_args = self.SHUTDOWN_COMMAND_ARGS.get(distribution, self.SHUTDOWN_COMMAND_ARGS['linux'])
    pre_reboot_delay = int(self._task.args.get('pre_reboot_delay', self.DEFAULT_PRE_REBOOT_DELAY))
    if (pre_reboot_delay < 0):
        pre_reboot_delay = 0
    delay_min = (pre_reboot_delay // 60)
    delay_min_macos = (delay_min | 1)
    msg = self._task.args.get('msg', self.DEFAULT_REBOOT_MESSAGE)
    shutdown_command_args = shutdown_command_args.format(delay_sec=pre_reboot_delay, delay_min=delay_min, delay_min_macos=delay_min_macos, message=msg)
    reboot_command = ('%s %s' % (shutdown_command, shutdown_command_args))
    return reboot_command