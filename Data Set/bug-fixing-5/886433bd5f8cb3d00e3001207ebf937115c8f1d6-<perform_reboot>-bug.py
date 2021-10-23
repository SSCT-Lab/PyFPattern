def perform_reboot(self):
    display.debug(('%s: rebooting server' % self._task.action))
    remote_command = self.construct_command()
    reboot_result = self._low_level_execute_command(remote_command, sudoable=self.DEFAULT_SUDOABLE)
    result = {
        
    }
    result['start'] = datetime.utcnow()
    if (reboot_result['rc'] != 0):
        result['failed'] = True
        result['rebooted'] = False
        result['msg'] = ('Shutdown command failed. Error was %s, %s' % (to_native(reboot_result['stdout'].strip()), to_native(reboot_result['stderr'].strip())))
        return result
    result['failed'] = False
    self._original_connection_timeout = None
    try:
        self._original_connection_timeout = self._connection.get_option('connection_timeout')
    except AnsibleError:
        display.debug(('%s: connect_timeout connection option has not been set' % self._task.action))
    return result