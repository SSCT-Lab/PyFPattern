def __attach_disks(self, entity):
    if (not self.param('disks')):
        return
    vm_service = self._service.service(entity.id)
    disks_service = self._connection.system_service().disks_service()
    disk_attachments_service = vm_service.disk_attachments_service()
    self._wait_for_vm_disks(vm_service)
    for disk in self.param('disks'):
        disk_id = disk.get('id')
        if (disk_id is None):
            disk_id = getattr(search_by_name(service=disks_service, name=disk.get('name')), 'id', None)
        disk_attachment = disk_attachments_service.attachment_service(disk_id)
        if (get_entity(disk_attachment) is None):
            if (not self._module.check_mode):
                disk_attachments_service.add(otypes.DiskAttachment(disk=otypes.Disk(id=disk_id), active=disk.get('activate', True), interface=otypes.DiskInterface(disk.get('interface', 'virtio')), bootable=disk.get('bootable', False)))
            self.changed = True