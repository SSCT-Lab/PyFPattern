def create_instance(module, proxmox, vmid, node, disk, storage, cpus, memory, swap, timeout, **kwargs):
    proxmox_node = proxmox.nodes(node)
    kwargs = dict(((k, v) for (k, v) in kwargs.items() if (v is not None)))
    if (VZ_TYPE == 'lxc'):
        kwargs['cpulimit'] = cpus
        kwargs['rootfs'] = disk
        if ('netif' in kwargs):
            kwargs.update(kwargs['netif'])
            del kwargs['netif']
        if ('mounts' in kwargs):
            kwargs.update(kwargs['mounts'])
            del kwargs['mounts']
        if ('pubkey' in kwargs):
            if (float(proxmox.version.get()['version']) >= 4.2):
                kwargs['ssh-public-keys'] = kwargs['pubkey']
            del kwargs['pubkey']
    else:
        kwargs['cpus'] = cpus
        kwargs['disk'] = disk
    taskid = getattr(proxmox_node, VZ_TYPE).create(vmid=vmid, storage=storage, memory=memory, swap=swap, **kwargs)
    while timeout:
        if ((proxmox_node.tasks(taskid).status.get()['status'] == 'stopped') and (proxmox_node.tasks(taskid).status.get()['exitstatus'] == 'OK')):
            return True
        timeout = (timeout - 1)
        if (timeout == 0):
            module.fail_json(msg=('Reached timeout while waiting for creating VM. Last line in task before timeout: %s' % proxmox_node.tasks(taskid).log.get()[:1]))
        time.sleep(1)
    return False