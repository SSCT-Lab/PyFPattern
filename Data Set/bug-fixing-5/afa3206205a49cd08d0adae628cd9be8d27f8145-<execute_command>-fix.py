def execute_command(content, vm, params):
    vm_username = params['vm_username']
    vm_password = params['vm_password']
    program_path = params['vm_shell']
    args = params['vm_shell_args']
    env = params['vm_shell_env']
    cwd = params['vm_shell_cwd']
    creds = vim.vm.guest.NamePasswordAuthentication(username=vm_username, password=vm_password)
    cmdspec = vim.vm.guest.ProcessManager.ProgramSpec(arguments=args, envVariables=env, programPath=program_path, workingDirectory=cwd)
    cmdpid = content.guestOperationsManager.processManager.StartProgramInGuest(vm=vm, auth=creds, spec=cmdspec)
    return cmdpid