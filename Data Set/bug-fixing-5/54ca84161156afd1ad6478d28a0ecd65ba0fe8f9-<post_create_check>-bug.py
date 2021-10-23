def post_create_check(self, sd_id):
    storage_domain = self._service.service(sd_id).get()
    self._service = self._attached_sds_service()
    attached_sd_service = self._service.service(storage_domain.id)
    if (get_entity(attached_sd_service) is None):
        self._service.add(otypes.StorageDomain(id=storage_domain.id))
        self.changed = True
        wait(service=attached_sd_service, condition=(lambda sd: (sd.status == sdstate.ACTIVE)), wait=self._module.params['wait'], timeout=self._module.params['timeout'])