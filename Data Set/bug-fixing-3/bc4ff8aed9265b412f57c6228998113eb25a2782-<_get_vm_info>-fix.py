def _get_vm_info(vm_name=None):
    "\n    Get all information of VM from vcsim\n    :param vm_name: Name of VM\n    :return: Dictionary containing information about VM,\n             where KEY represent attributes and VALUE represent attribute's value\n    "
    cmd = ('%s vm.info %s 2>&1' % (GOVCPATH, vm_name))
    vm_info = {
        
    }
    if (vm_name is None):
        return vm_info
    vm_info = parse_govc_info(cmd)
    return vm_info