def _get_vm_info(vm_name=None):
    "\n    Get all information of VM from vcsim\n    :param vm_name: Name of VM\n    :return: Dictionary containing inforamtion about VM,\n             where KEY represent attributes and VALUE represent attribute's value\n    "
    cmd = ('%s vm.info %s 2>&1' % (GOVCPATH, vm_name))
    (so, se) = run_cmd(cmd)
    stdout_lines = so.splitlines()
    vm_info = {
        
    }
    if (vm_name is None):
        return vm_info
    for line in stdout_lines:
        if (':' in line):
            (key, value) = line.split(':')
            key = key.lstrip()
            vm_info[key] = value.strip()
    return vm_info