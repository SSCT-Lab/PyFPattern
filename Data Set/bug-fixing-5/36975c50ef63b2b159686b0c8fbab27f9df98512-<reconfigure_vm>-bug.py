def reconfigure_vm(vsphere_client, vm, module, esxi, resource_pool, cluster_name, guest, vm_extra_config, vm_hardware, vm_disk, vm_nic, state, force):
    spec = None
    changed = False
    changes = {
        
    }
    request = None
    shutdown = False
    poweron = vm.is_powered_on()
    devices = []
    memoryHotAddEnabled = bool(vm.properties.config.memoryHotAddEnabled)
    cpuHotAddEnabled = bool(vm.properties.config.cpuHotAddEnabled)
    cpuHotRemoveEnabled = bool(vm.properties.config.cpuHotRemoveEnabled)
    (changed, changes) = update_disks(vsphere_client, vm, module, vm_disk, changes)
    request = VI.ReconfigVM_TaskRequestMsg()
    if vm_extra_config:
        spec = spec_singleton(spec, request, vm)
        extra_config = []
        for (k, v) in vm_extra_config.items():
            ec = spec.new_extraConfig()
            ec.set_element_key(str(k))
            ec.set_element_value(str(v))
            extra_config.append(ec)
        spec.set_element_extraConfig(extra_config)
        changes['extra_config'] = vm_extra_config
    if ('memory_mb' in vm_hardware):
        if (int(vm_hardware['memory_mb']) != vm.properties.config.hardware.memoryMB):
            spec = spec_singleton(spec, request, vm)
            if vm.is_powered_on():
                if force:
                    if (not memoryHotAddEnabled):
                        shutdown = True
                    elif (int(vm_hardware['memory_mb']) < vm.properties.config.hardware.memoryMB):
                        shutdown = True
                elif (not memoryHotAddEnabled):
                    module.fail_json(msg='memoryHotAdd is not enabled. force is required for shutdown')
                elif (int(vm_hardware['memory_mb']) < vm.properties.config.hardware.memoryMB):
                    module.fail_json(msg='Cannot lower memory on a live VM. force is required for shutdown')
            spec.set_element_memoryMB(int(vm_hardware['memory_mb']))
            changes['memory'] = vm_hardware['memory_mb']
    if vm_nic:
        changed = reconfigure_net(vsphere_client, vm, module, esxi, resource_pool, guest, vm_nic, cluster_name)
    if ('num_cpus' in vm_hardware):
        if (int(vm_hardware['num_cpus']) != vm.properties.config.hardware.numCPU):
            spec = spec_singleton(spec, request, vm)
            if vm.is_powered_on():
                if force:
                    if (not cpuHotAddEnabled):
                        shutdown = True
                    elif (int(vm_hardware['num_cpus']) < vm.properties.config.hardware.numCPU):
                        if (not cpuHotRemoveEnabled):
                            shutdown = True
                elif (not cpuHotAddEnabled):
                    module.fail_json(msg='cpuHotAdd is not enabled. force is required for shutdown')
                elif (int(vm_hardware['num_cpus']) < vm.properties.config.hardware.numCPU):
                    if (not cpuHotRemoveEnabled):
                        module.fail_json(msg='Cannot lower CPU on a live VM without cpuHotRemove. force is required for shutdown')
            spec.set_element_numCPUs(int(vm_hardware['num_cpus']))
            changes['cpu'] = vm_hardware['num_cpus']
    if ('vm_cdrom' in vm_hardware):
        spec = spec_singleton(spec, request, vm)
        (cdrom_type, cdrom_iso_path) = get_cdrom_params(module, vsphere_client, vm_hardware['vm_cdrom'])
        cdrom = None
        current_devices = vm.properties.config.hardware.device
        for dev in current_devices:
            if (dev._type == 'VirtualCdrom'):
                cdrom = dev._obj
                break
        if (cdrom_type == 'iso'):
            iso_location = cdrom_iso_path.split('/', 1)
            (datastore, ds) = find_datastore(module, vsphere_client, iso_location[0], None)
            iso_path = iso_location[1]
            iso = VI.ns0.VirtualCdromIsoBackingInfo_Def('iso').pyclass()
            iso.set_element_fileName(('%s %s' % (datastore, iso_path)))
            cdrom.set_element_backing(iso)
            cdrom.Connectable.set_element_connected(True)
            cdrom.Connectable.set_element_startConnected(True)
        elif (cdrom_type == 'client'):
            client = VI.ns0.VirtualCdromRemoteAtapiBackingInfo_Def('client').pyclass()
            client.set_element_deviceName('')
            cdrom.set_element_backing(client)
            cdrom.Connectable.set_element_connected(True)
            cdrom.Connectable.set_element_startConnected(True)
        else:
            vsphere_client.disconnect()
            module.fail_json(msg=('Error adding cdrom of type %s to vm spec.  cdrom type can either be iso or client' % cdrom_type))
        dev_change = spec.new_deviceChange()
        dev_change.set_element_device(cdrom)
        dev_change.set_element_operation('edit')
        devices.append(dev_change)
        changes['cdrom'] = vm_hardware['vm_cdrom']
    if vm_disk:
        spec = spec_singleton(spec, request, vm)
        dev_list = [d for d in vm.properties.config.hardware.device if (d._type == 'VirtualDisk')]
        if (len(vm_disk) > len(dev_list)):
            vsphere_client.disconnect()
            module.fail_json(msg="Error in vm_disk definition. Too many disks defined in comparison to the VM's disk profile.")
        disk_num = 0
        dev_changes = []
        disks_changed = {
            
        }
        for disk in sorted(vm_disk):
            try:
                disksize = int(vm_disk[disk]['size_gb'])
                disksize = ((disksize * 1024) * 1024)
            except (KeyError, ValueError):
                vsphere_client.disconnect()
                module.fail_json(msg=("Error in '%s' definition. Size needs to be specified as an integer." % disk))
            dev = dev_list[disk_num]
            if (disksize < int(dev.capacityInKB)):
                vsphere_client.disconnect()
                module.fail_json(msg=("Error in '%s' definition. New size needs to be higher than the current value (%s GB)." % (disk, ((int(dev.capacityInKB) / 1024) / 1024))))
            elif (disksize > int(dev.capacityInKB)):
                dev_obj = dev._obj
                dev_obj.set_element_capacityInKB(disksize)
                dev_change = spec.new_deviceChange()
                dev_change.set_element_operation('edit')
                dev_change.set_element_device(dev_obj)
                dev_changes.append(dev_change)
                disks_changed[disk] = {
                    'size_gb': int(vm_disk[disk]['size_gb']),
                }
            disk_num = (disk_num + 1)
        if dev_changes:
            spec.set_element_deviceChange(dev_changes)
            changes['disks'] = disks_changed
    if len(changes):
        if (shutdown and vm.is_powered_on()):
            try:
                vm.power_off(sync_run=True)
                vm.get_status()
            except Exception:
                e = get_exception()
                module.fail_json(msg=('Failed to shutdown vm %s: %s' % (guest, e)))
        if len(devices):
            spec.set_element_deviceChange(devices)
        request.set_element_spec(spec)
        ret = vsphere_client._proxy.ReconfigVM_Task(request)._returnval
        task = VITask(ret, vsphere_client)
        status = task.wait_for_state([task.STATE_SUCCESS, task.STATE_ERROR])
        if (status == task.STATE_SUCCESS):
            changed = True
        elif (status == task.STATE_ERROR):
            module.fail_json(msg=('Error reconfiguring vm: %s' % task.get_error_message()))
        if (vm.is_powered_off() and poweron):
            try:
                vm.power_on(sync_run=True)
            except Exception:
                e = get_exception()
                module.fail_json(msg=('Failed to power on vm %s : %s' % (guest, e)))
    vsphere_client.disconnect()
    if changed:
        module.exit_json(changed=True, changes=changes)
    module.exit_json(changed=False)