def get_system_boot_time(self):
    stdout = ''
    stderr = ''
    command_result = self._low_level_execute_command(self.DEFAULT_BOOT_TIME_COMMAND, sudoable=self.DEFAULT_SUDOABLE)
    if ('1970-01-01 00:00' in command_result['stdout']):
        stdout += command_result['stdout']
        stderr += command_result['stderr']
        command_result = self._low_level_execute_command('uptime -s', sudoable=self.DEFAULT_SUDOABLE)
    if (command_result['rc'] != 0):
        stdout += command_result['stdout']
        stderr += command_result['stderr']
        command_result = self._low_level_execute_command('cat /proc/sys/kernel/random/boot_id', sudoable=self.DEFAULT_SUDOABLE)
    if (command_result['rc'] != 0):
        stdout += command_result['stdout']
        stderr += command_result['stderr']
        raise AnsibleError(('%s: failed to get host boot time info, rc: %d, stdout: %s, stderr: %s' % (self._task.action, command_result['rc'], to_native(stdout), to_native(stderr))))
    return command_result['stdout'].strip()