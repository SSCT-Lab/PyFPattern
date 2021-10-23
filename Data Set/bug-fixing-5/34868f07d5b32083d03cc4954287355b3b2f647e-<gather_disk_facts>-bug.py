def gather_disk_facts(self, vm_obj):
    "\n        Gather facts about VM's disks\n        Args:\n            vm_obj: Managed object of virtual machine\n\n        Returns: A list of dict containing disks information\n\n        "
    disks_facts = dict()
    if (vm_obj is None):
        return disks_facts
    disk_index = 0
    for disk in vm_obj.config.hardware.device:
        if isinstance(disk, vim.vm.device.VirtualDisk):
            disks_facts[disk_index] = dict(key=disk.key, label=disk.deviceInfo.label, summary=disk.deviceInfo.summary, backing_filename=disk.backing.fileName, backing_datastore=disk.backing.datastore.name, backing_disk_mode=disk.backing.diskMode, backing_writethrough=disk.backing.writeThrough, backing_thinprovisioned=disk.backing.thinProvisioned, backing_uuid=disk.backing.uuid, backing_eagerlyscrub=bool(disk.backing.eagerlyScrub), controller_key=disk.controllerKey, unit_number=disk.unitNumber, capacity_in_kb=disk.capacityInKB, capacity_in_bytes=disk.capacityInBytes)
            disk_index += 1
    return disks_facts