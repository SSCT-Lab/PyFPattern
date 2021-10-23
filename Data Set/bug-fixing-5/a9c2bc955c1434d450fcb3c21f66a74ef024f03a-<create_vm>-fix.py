def create_vm(module, proxmox, vmid, newid, node, name, memory, cpu, cores, sockets, timeout, update, **kwargs):
    only_v4 = ['force', 'protection', 'skiplock']
    valid_clone_params = ['format', 'full', 'pool', 'snapname', 'storage', 'target']
    clone_params = {
        
    }
    vm_args = '-serial unix:/var/run/qemu-server/{}.serial,server,nowait'.format(vmid)
    proxmox_node = proxmox.nodes(node)
    kwargs = dict(((k, v) for (k, v) in kwargs.items() if (v is not None)))
    kwargs.update(dict(([k, int(v)] for (k, v) in kwargs.items() if isinstance(v, bool))))
    if (PVE_MAJOR_VERSION < 4):
        for p in only_v4:
            if (p in kwargs):
                del kwargs[p]
    if update:
        if ('virtio' in kwargs):
            del kwargs['virtio']
        if ('sata' in kwargs):
            del kwargs['sata']
        if ('scsi' in kwargs):
            del kwargs['scsi']
        if ('ide' in kwargs):
            del kwargs['ide']
        if ('net' in kwargs):
            del kwargs['net']
    for k in list(kwargs.keys()):
        if isinstance(kwargs[k], dict):
            kwargs.update(kwargs[k])
            del kwargs[k]
    if ('numa_enabled' in kwargs):
        kwargs['numa'] = kwargs['numa_enabled']
        del kwargs['numa_enabled']
    if ((module.params['api_user'] == 'root@pam') and (module.params['args'] is None)):
        if (not update):
            kwargs['args'] = vm_args
    elif ((module.params['api_user'] == 'root@pam') and (module.params['args'] is not None)):
        kwargs['args'] = module.params['args']
    elif ((module.params['api_user'] != 'root@pam') and (module.params['args'] is not None)):
        module.fail_json(msg='args parameter require root@pam user. ')
    if ((module.params['api_user'] != 'root@pam') and (module.params['skiplock'] is not None)):
        module.fail_json(msg='skiplock parameter require root@pam user. ')
    if update:
        if (getattr(proxmox_node, VZ_TYPE)(vmid).config.set(name=name, memory=memory, cpu=cpu, cores=cores, sockets=sockets, **kwargs) is None):
            return True
        else:
            return False
    elif (module.params['clone'] is not None):
        for param in valid_clone_params:
            if (module.params[param] is not None):
                clone_params[param] = module.params[param]
        clone_params.update(dict(([k, int(v)] for (k, v) in clone_params.items() if isinstance(v, bool))))
        taskid = proxmox_node.qemu(vmid).clone.post(newid=newid, name=name, **clone_params)
    else:
        taskid = getattr(proxmox_node, VZ_TYPE).create(vmid=vmid, name=name, memory=memory, cpu=cpu, cores=cores, sockets=sockets, **kwargs)
    while timeout:
        if ((proxmox_node.tasks(taskid).status.get()['status'] == 'stopped') and (proxmox_node.tasks(taskid).status.get()['exitstatus'] == 'OK')):
            return True
        timeout = (timeout - 1)
        if (timeout == 0):
            module.fail_json(msg=('Reached timeout while waiting for creating VM. Last line in task before timeout: %s' % proxmox_node.tasks(taskid).log.get()[:1]))
        time.sleep(1)
    return False