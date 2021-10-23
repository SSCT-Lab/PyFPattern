def run_command_in_guest(self, vm, username, password, program_path, program_args, program_cwd, program_env):
    result = {
        'failed': False,
    }
    tools_status = vm.guest.toolsStatus
    if ((tools_status == 'toolsNotInstalled') or (tools_status == 'toolsNotRunning')):
        result['failed'] = True
        result['msg'] = 'VMwareTools is not installed or is not running in the guest'
        return result
    creds = vim.vm.guest.NamePasswordAuthentication(username=username, password=password)
    try:
        pm = self.content.guestOperationsManager.processManager
        ps = vim.vm.guest.ProcessManager.ProgramSpec(programPath=program_path, arguments=program_args, workingDirectory=program_cwd)
        res = pm.StartProgramInGuest(vm, creds, ps)
        result['pid'] = res
        pdata = pm.ListProcessesInGuest(vm, creds, [res])
        while (not pdata[0].endTime):
            time.sleep(1)
            pdata = pm.ListProcessesInGuest(vm, creds, [res])
        result['owner'] = pdata[0].owner
        result['startTime'] = pdata[0].startTime.isoformat()
        result['endTime'] = pdata[0].endTime.isoformat()
        result['exitCode'] = pdata[0].exitCode
        if (result['exitCode'] != 0):
            result['failed'] = True
            result['msg'] = 'program exited non-zero'
        else:
            result['msg'] = 'program completed successfully'
    except Exception as e:
        result['msg'] = str(e)
        result['failed'] = True
    return result