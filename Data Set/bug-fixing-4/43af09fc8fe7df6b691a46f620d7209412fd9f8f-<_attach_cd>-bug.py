def _attach_cd(self, entity):
    cd_iso = self.param('cd_iso')
    if (cd_iso is not None):
        vm_service = self._service.service(entity.id)
        current = (vm_service.get().status == otypes.VmStatus.UP)
        cdroms_service = vm_service.cdroms_service()
        cdrom_device = cdroms_service.list()[0]
        cdrom_service = cdroms_service.cdrom_service(cdrom_device.id)
        cdrom = cdrom_service.get(current=current)
        if (getattr(cdrom.file, 'id', '') != cd_iso):
            if (not self._module.check_mode):
                cdrom_service.update(cdrom=otypes.Cdrom(file=otypes.File(id=cd_iso)), current=current)
            self.changed = True
    return entity