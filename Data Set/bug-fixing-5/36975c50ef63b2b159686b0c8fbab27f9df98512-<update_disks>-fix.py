def update_disks(vsphere_client, vm, module, vm_disk, changes):
    request = VI.ReconfigVM_TaskRequestMsg()
    changed = False
    for cnf_disk in vm_disk:
        disk_id = re.sub('disk', '', cnf_disk)
        disk_type = vm_disk[cnf_disk]['type']
        found = False
        for dev_key in vm._devices:
            if (vm._devices[dev_key]['type'] == 'VirtualDisk'):
                hdd_id = vm._devices[dev_key]['label'].split()[2]
                if (disk_id == hdd_id):
                    found = True
                    continue
        if (not found):
            it = VI.ReconfigVM_TaskRequestMsg()
            _this = request.new__this(vm._mor)
            _this.set_attribute_type(vm._mor.get_attribute_type())
            request.set_element__this(_this)
            spec = request.new_spec()
            dc = spec.new_deviceChange()
            dc.Operation = 'add'
            dc.FileOperation = 'create'
            hd = VI.ns0.VirtualDisk_Def('hd').pyclass()
            hd.Key = (- 100)
            hd.UnitNumber = int(disk_id)
            hd.CapacityInKB = ((int(vm_disk[cnf_disk]['size_gb']) * 1024) * 1024)
            hd.ControllerKey = 1000
            backing = VI.ns0.VirtualDiskFlatVer2BackingInfo_Def('backing').pyclass()
            backing.FileName = ('[%s]' % vm_disk[cnf_disk]['datastore'])
            backing.DiskMode = 'persistent'
            backing.Split = False
            backing.WriteThrough = False
            if (disk_type == 'thin'):
                backing.ThinProvisioned = True
            else:
                backing.ThinProvisioned = False
            backing.EagerlyScrub = False
            hd.Backing = backing
            dc.Device = hd
            spec.DeviceChange = [dc]
            request.set_element_spec(spec)
            ret = vsphere_client._proxy.ReconfigVM_Task(request)._returnval
            task = VITask(ret, vsphere_client)
            status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
            if (status == task.STATE_SUCCESS):
                changed = True
                changes[cnf_disk] = vm_disk[cnf_disk]
            elif (status == task.STATE_ERROR):
                module.fail_json(msg=('Error reconfiguring vm: %s, [%s]' % (task.get_error_message(), vm_disk[cnf_disk])))
    return (changed, changes)