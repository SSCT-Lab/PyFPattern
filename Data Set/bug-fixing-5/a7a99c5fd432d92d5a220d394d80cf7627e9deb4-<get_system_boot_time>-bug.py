def get_system_boot_time(self):
    command_result = self._low_level_execute_command(self.DEFAULT_BOOT_TIME_COMMAND, sudoable=self.DEFAULT_SUDOABLE)
    if ('1970-01-01 00:00' in command_result['stdout']):
        command_result = self._low_level_execute_command('uptime -s', sudoable=self.DEFAULT_SUDOABLE)
    if (command_result['rc'] != 0):
        raise AnsibleError(('%s: failed to get host boot time info, rc: %d, stdout: %s, stderr: %s' % (self._task.action, command_result.rc, to_native(command_result['stdout']), to_native(command_result['stderr']))))
    return command_result['stdout'].strip()