def configure_disks(self, vm_obj):
    if (len(self.params['disk']) == 0):
        return
    scsi_ctl = self.get_vm_scsi_controller(vm_obj)
    if ((vm_obj is None) or (scsi_ctl is None)):
        scsi_ctl = self.device_helper.create_scsi_controller(self.get_scsi_type())
        self.change_detected = True
        self.configspec.deviceChange.append(scsi_ctl)
    disks = ([x for x in vm_obj.config.hardware.device if isinstance(x, vim.vm.device.VirtualDisk)] if (vm_obj is not None) else None)
    if ((disks is not None) and self.params.get('disk') and (len(self.params.get('disk')) < len(disks))):
        self.module.fail_json(msg=('Provided disks configuration has less disks than the target object (%d vs %d)' % (len(self.params.get('disk')), len(disks))))
    disk_index = 0
    for expected_disk_spec in self.params.get('disk'):
        disk_modified = False
        if ((vm_obj is not None) and (disks is not None) and (disk_index < len(disks))):
            diskspec = vim.vm.device.VirtualDeviceSpec()
            diskspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
            diskspec.device = disks[disk_index]
        else:
            diskspec = self.device_helper.create_scsi_disk(scsi_ctl, disk_index)
            disk_modified = True
        disk_index += 1
        if (disk_index == 7):
            disk_index += 1
        if ('disk_mode' in expected_disk_spec):
            disk_mode = expected_disk_spec.get('disk_mode', 'persistent').lower()
            valid_disk_mode = ['persistent', 'independent_persistent', 'independent_nonpersistent']
            if (disk_mode not in valid_disk_mode):
                self.module.fail_json(msg=("disk_mode specified is not valid. Should be one of ['%s']" % "', '".join(valid_disk_mode)))
            if ((vm_obj and (diskspec.device.backing.diskMode != disk_mode)) or (vm_obj is None)):
                diskspec.device.backing.diskMode = disk_mode
                disk_modified = True
        else:
            diskspec.device.backing.diskMode = 'persistent'
        if ('type' in expected_disk_spec):
            disk_type = expected_disk_spec.get('type', '').lower()
            if (disk_type == 'thin'):
                diskspec.device.backing.thinProvisioned = True
            elif (disk_type == 'eagerzeroedthick'):
                diskspec.device.backing.eagerlyScrub = True
        if (('filename' in expected_disk_spec) and (expected_disk_spec['filename'] is not None)):
            self.add_existing_vmdk(vm_obj, expected_disk_spec, diskspec, scsi_ctl)
            continue
        else:
            diskspec.fileOperation = vim.vm.device.VirtualDeviceSpec.FileOperation.create
        if expected_disk_spec.get('datastore'):
            pass
        kb = self.get_configured_disk_size(expected_disk_spec)
        if (kb < diskspec.device.capacityInKB):
            self.module.fail_json(msg=('Given disk size is smaller than found (%d < %d). Reducing disks is not allowed.' % (kb, diskspec.device.capacityInKB)))
        if ((kb != diskspec.device.capacityInKB) or disk_modified):
            diskspec.device.capacityInKB = kb
            self.configspec.deviceChange.append(diskspec)
            self.change_detected = True