def _get_pid_info(self, pid):
    try:
        processes = self.processManager.ListProcessesInGuest(vm=self.vm, auth=self.vm_auth, pids=[pid])
    except vim.fault.NoPermission as e:
        raise AnsibleError(('No Permission Error: %s %s' % (to_native(e.msg), to_native(e.privilegeId))))
    return processes[0]