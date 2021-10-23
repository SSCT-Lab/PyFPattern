def process_exists_in_guest(self, vm, pid, creds):
    res = self.pm.ListProcessesInGuest(vm, creds, pids=[pid])
    if (not res):
        return (False, '')
    res = res[0]
    if (res.exitCode is None):
        return (True, '')
    elif (res.exitCode >= 0):
        return (False, res)
    else:
        return (True, res)