def execute_command(content, vm, vm_username, vm_password, program_path, args='', env=None, cwd=None):
    creds = vim.vm.guest.NamePasswordAuthentication(username=vm_username, password=vm_password)
    cmdspec = vim.vm.guest.ProcessManager.ProgramSpec(arguments=args, envVariables=env, programPath=program_path, workingDirectory=cwd)
    cmdpid = content.guestOperationsManager.processManager.StartProgramInGuest(vm=vm, auth=creds, spec=cmdspec)
    return cmdpid