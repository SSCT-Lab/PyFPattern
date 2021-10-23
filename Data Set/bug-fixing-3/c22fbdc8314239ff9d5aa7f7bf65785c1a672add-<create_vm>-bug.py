def create_vm(module, proxmox, vmid, node, name, memory, cpu, cores, sockets, timeout, **kwargs):
    only_v4 = ['force', 'protection', 'skiplock']
    vm_args = '-serial unix:/var/run/qemu-server/{}.serial,server,nowait'.format(vmid)
    proxmox_node = proxmox.nodes(node)
    kwargs = dict(((k, v) for (k, v) in kwargs.items() if (v is not None)))
    kwargs.update(dict(([k, int(v)] for (k, v) in kwargs.items() if isinstance(v, bool))))
    if (PVE_MAJOR_VERSION < 4):
        for p in only_v4:
            if (p in kwargs):
                del kwargs[p]
    for k in kwargs.keys():
        if isinstance(kwargs[k], dict):
            kwargs.update(kwargs[k])
            del kwargs[k]
    if ((module.params['api_user'] == 'root@pam') and (module.params['args'] is None)):
        kwargs['args'] = vm_args
    elif ((module.params['api_user'] == 'root@pam') and (module.params['args'] is not None)):
        kwargs['args'] = module.params['args']
    elif ((module.params['api_user'] != 'root@pam') and (module.params['args'] is not None)):
        module.fail_json(msg='args parameter require root@pam user. ')
    if ((module.params['api_user'] != 'root@pam') and (module.params['skiplock'] is not None)):
        module.fail_json(msg='skiplock parameter require root@pam user. ')
    taskid = getattr(proxmox_node, VZ_TYPE).create(vmid=vmid, name=name, memory=memory, cpu=cpu, cores=cores, sockets=sockets, **kwargs)
    while timeout:
        if ((proxmox_node.tasks(taskid).status.get()['status'] == 'stopped') and (proxmox_node.tasks(taskid).status.get()['exitstatus'] == 'OK')):
            return True
        timeout = (timeout - 1)
        if (timeout == 0):
            module.fail_json(msg=('Reached timeout while waiting for creating VM. Last line in task before timeout: %s' % proxmox_node.tasks(taskid).log.get()[:1]))
        time.sleep(1)
    return False