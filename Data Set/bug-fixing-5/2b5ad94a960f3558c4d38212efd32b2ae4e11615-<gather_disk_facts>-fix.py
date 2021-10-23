def gather_disk_facts(self, vm_obj):
    "\n        Gather facts about VM's disks\n        Args:\n            vm_obj: Managed object of virtual machine\n\n        Returns: A list of dict containing disks information\n\n        "
    controller_facts = dict()
    disks_facts = dict()
    if (vm_obj is None):
        return disks_facts
    controller_types = {
        vim.vm.device.VirtualLsiLogicController: 'lsilogic',
        vim.vm.device.ParaVirtualSCSIController: 'paravirtual',
        vim.vm.device.VirtualBusLogicController: 'buslogic',
        vim.vm.device.VirtualLsiLogicSASController: 'lsilogicsas',
        vim.vm.device.VirtualIDEController: 'ide',
    }
    controller_index = 0
    for controller in vm_obj.config.hardware.device:
        if isinstance(controller, tuple(controller_types.keys())):
            controller_facts[controller_index] = dict(key=controller.key, controller_type=controller_types[type(controller)], bus_number=controller.busNumber, devices=controller.device)
            controller_index += 1
    disk_index = 0
    for disk in vm_obj.config.hardware.device:
        if isinstance(disk, vim.vm.device.VirtualDisk):
            disks_facts[disk_index] = dict(key=disk.key, label=disk.deviceInfo.label, summary=disk.deviceInfo.summary, backing_filename=disk.backing.fileName, backing_datastore=disk.backing.datastore.name, controller_key=disk.controllerKey, unit_number=disk.unitNumber, capacity_in_kb=disk.capacityInKB, capacity_in_bytes=disk.capacityInBytes)
            if isinstance(disk.backing, vim.vm.device.VirtualDisk.FlatVer1BackingInfo):
                disks_facts[disk_index]['backing_type'] = 'FlatVer1'
                disks_facts[disk_index]['backing_writethrough'] = disk.backing.writeThrough
            elif isinstance(disk.backing, vim.vm.device.VirtualDisk.FlatVer2BackingInfo):
                disks_facts[disk_index]['backing_type'] = 'FlatVer2'
                disks_facts[disk_index]['backing_writethrough'] = bool(disk.backing.writeThrough)
                disks_facts[disk_index]['backing_thinprovisioned'] = bool(disk.backing.thinProvisioned)
                disks_facts[disk_index]['backing_eagerlyscrub'] = bool(disk.backing.eagerlyScrub)
                disks_facts[disk_index]['backing_uuid'] = disk.backing.uuid
            elif isinstance(disk.backing, vim.vm.device.VirtualDisk.LocalPMemBackingInfo):
                disks_facts[disk_index]['backing_type'] = 'LocalPMem'
                disks_facts[disk_index]['backing_volumeuuid'] = disk.backing.volumeUUID
                disks_facts[disk_index]['backing_uuid'] = disk.backing.uuid
            elif isinstance(disk.backing, vim.vm.device.VirtualDisk.PartitionedRawDiskVer2BackingInfo):
                disks_facts[disk_index]['backing_type'] = 'PartitionedRawDiskVer2'
                disks_facts[disk_index]['backing_descriptorfilename'] = disk.backing.descriptorFileName
                disks_facts[disk_index]['backing_uuid'] = disk.backing.uuid
            elif isinstance(disk.backing, vim.vm.device.VirtualDisk.RawDiskMappingVer1BackingInfo):
                disks_facts[disk_index]['backing_type'] = 'RawDiskMappingVer1'
                disks_facts[disk_index]['backing_devicename'] = disk.backing.deviceName
                disks_facts[disk_index]['backing_diskmode'] = disk.backing.diskMode
                disks_facts[disk_index]['backing_lunuuid'] = disk.backing.lunUuid
                disks_facts[disk_index]['backing_uuid'] = disk.backing.uuid
            elif isinstance(disk.backing, vim.vm.device.VirtualDisk.RawDiskVer2BackingInfo):
                disks_facts[disk_index]['backing_type'] = 'RawDiskVer2'
                disks_facts[disk_index]['backing_descriptorfilename'] = disk.backing.descriptorFileName
                disks_facts[disk_index]['backing_uuid'] = disk.backing.uuid
            elif isinstance(disk.backing, vim.vm.device.VirtualDisk.SeSparseBackingInfo):
                disks_facts[disk_index]['backing_type'] = 'SeSparse'
                disks_facts[disk_index]['backing_diskmode'] = disk.backing.diskMode
                disks_facts[disk_index]['backing_writethrough'] = bool(disk.backing.writeThrough)
                disks_facts[disk_index]['backing_uuid'] = disk.backing.uuid
            elif isinstance(disk.backing, vim.vm.device.VirtualDisk.SparseVer1BackingInfo):
                disks_facts[disk_index]['backing_type'] = 'SparseVer1'
                disks_facts[disk_index]['backing_diskmode'] = disk.backing.diskMode
                disks_facts[disk_index]['backing_spaceusedinkb'] = disk.backing.spaceUsedInKB
                disks_facts[disk_index]['backing_split'] = bool(disk.backing.split)
                disks_facts[disk_index]['backing_writethrough'] = bool(disk.backing.writeThrough)
            elif isinstance(disk.backing, vim.vm.device.VirtualDisk.SparseVer2BackingInfo):
                disks_facts[disk_index]['backing_type'] = 'SparseVer2'
                disks_facts[disk_index]['backing_diskmode'] = disk.backing.diskMode
                disks_facts[disk_index]['backing_spaceusedinkb'] = disk.backing.spaceUsedInKB
                disks_facts[disk_index]['backing_split'] = bool(disk.backing.split)
                disks_facts[disk_index]['backing_writethrough'] = bool(disk.backing.writeThrough)
                disks_facts[disk_index]['backing_uuid'] = disk.backing.uuid
            for controller_index in range(len(controller_facts)):
                if (controller_facts[controller_index]['key'] == disks_facts[disk_index]['controller_key']):
                    disks_facts[disk_index]['controller_bus_number'] = controller_facts[controller_index]['bus_number']
                    disks_facts[disk_index]['controller_type'] = controller_facts[controller_index]['controller_type']
            disk_index += 1
    return disks_facts