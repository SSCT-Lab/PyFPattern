def get_vminfo(module, proxmox, node, vmid, **kwargs):
    global results
    results = {
        
    }
    mac = {
        
    }
    devices = {
        
    }
    try:
        vm = proxmox.nodes(node).qemu(vmid).config.get()
    except Exception as e:
        module.fail_json(msg=('Getting information for VM with vmid = %s failed with exception: %s' % (vmid, e)))
    kwargs = dict(((k, v) for (k, v) in kwargs.items() if (v is not None)))
    for k in list(kwargs.keys()):
        if isinstance(kwargs[k], dict):
            kwargs.update(kwargs[k])
            del kwargs[k]
    for (k, v) in kwargs.items():
        if (re.match('net[0-9]', k) is not None):
            interface = k
            k = vm[k]
            k = re.search('=(.*?),', k).group(1)
            mac[interface] = k
        if ((re.match('virtio[0-9]', k) is not None) or (re.match('ide[0-9]', k) is not None) or (re.match('scsi[0-9]', k) is not None) or (re.match('sata[0-9]', k) is not None)):
            device = k
            k = vm[k]
            k = re.search('(.*?),', k).group(1)
            devices[device] = k
    results['mac'] = mac
    results['devices'] = devices
    results['vmid'] = int(vmid)