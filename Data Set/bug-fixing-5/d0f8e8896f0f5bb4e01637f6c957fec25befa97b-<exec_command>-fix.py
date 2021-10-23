def exec_command(self, cmd, in_data=None, sudoable=True):
    'Execute command.'
    super(Connection, self).exec_command(cmd, in_data=in_data, sudoable=sudoable)
    stdout = self.create_temporary_file_in_guest(suffix='.stdout')
    stderr = self.create_temporary_file_in_guest(suffix='.stderr')
    guest_program_spec = self._get_guest_program_spec(cmd, stdout, stderr)
    try:
        pid = self.processManager.StartProgramInGuest(vm=self.vm, auth=self.vm_auth, spec=guest_program_spec)
    except vim.fault.NoPermission as e:
        raise AnsibleError(('No Permission Error: %s %s' % (to_native(e.msg), to_native(e.privilegeId))))
    except vim.fault.FileNotFound as e:
        raise AnsibleError(('StartProgramInGuest Error: %s' % to_native(e.msg)))
    except vmodl.fault.SystemError as e:
        if (e.reason == 'vix error codes = (3016, 0).\n'):
            raise AnsibleConnectionFailure(('Connection failed, is the vm currently rebooting? Reason: %s' % to_native(e.reason)))
        else:
            raise AnsibleConnectionFailure(('Connection failed. Reason %s' % to_native(e.reason)))
    except vim.fault.GuestOperationsUnavailable:
        raise AnsibleConnectionFailure('Cannot connect to guest. Native error: GuestOperationsUnavailable')
    pid_info = self._get_pid_info(pid)
    while (pid_info.endTime is None):
        sleep(self.get_option('exec_command_sleep_interval'))
        pid_info = self._get_pid_info(pid)
    stdout_response = self._fetch_file_from_vm(stdout)
    self.delete_file_in_guest(stdout)
    stderr_response = self._fetch_file_from_vm(stderr)
    self.delete_file_in_guest(stderr)
    return (pid_info.exitCode, stdout_response.text, stderr_response.text)