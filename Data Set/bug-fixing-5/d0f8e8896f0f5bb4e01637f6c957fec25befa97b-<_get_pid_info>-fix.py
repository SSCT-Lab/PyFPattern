def _get_pid_info(self, pid):
    try:
        processes = self.processManager.ListProcessesInGuest(vm=self.vm, auth=self.vm_auth, pids=[pid])
    except vim.fault.NoPermission as e:
        raise AnsibleError(('No Permission Error: %s %s' % (to_native(e.msg), to_native(e.privilegeId))))
    except vmodl.fault.SystemError as e:
        if (e.reason == 'vix error codes = (1, 0).\n'):
            raise AnsibleConnectionFailure(('Connection failed, Netlogon service stopped or dcpromo in progress. Reason: %s' % to_native(e.reason)))
        else:
            raise AnsibleConnectionFailure(('Connection plugin failed. Reason: %s' % to_native(e.reason)))
    except vim.fault.GuestOperationsUnavailable:
        raise AnsibleConnectionFailure('Cannot connect to guest. Native error: GuestOperationsUnavailable')
    except vim.fault.InvalidGuestLogin:
        raise AnsibleConnectionFailure('Guest login failed. Native error: InvalidGuestLogin')
    return processes[0]