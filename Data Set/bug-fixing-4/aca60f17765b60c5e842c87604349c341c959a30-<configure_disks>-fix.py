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
        if ('type' in expected_disk_spec):
            if (expected_disk_spec.get('type', '').lower() == 'thin'):
                diskspec.device.backing.thinProvisioned = True
        if expected_disk_spec.get('datastore'):
            pass
        disk_index += 1
        if (disk_index == 7):
            disk_index += 1
        kb = self.get_configured_disk_size(expected_disk_spec)
        if (kb < diskspec.device.capacityInKB):
            self.module.fail_json(msg=('Given disk size is lesser than found (%d < %d). Reducing disks is not allowed.' % (kb, diskspec.device.capacityInKB)))
        if ((kb != diskspec.device.capacityInKB) or disk_modified):
            diskspec.device.capacityInKB = kb
            self.configspec.deviceChange.append(diskspec)
            self.change_detected = True