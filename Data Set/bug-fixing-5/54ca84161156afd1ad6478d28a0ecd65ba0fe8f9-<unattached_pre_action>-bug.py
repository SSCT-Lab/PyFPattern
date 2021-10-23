def unattached_pre_action(self, storage_domain):
    self._service = self._attached_sds_service(storage_domain)
    self._maintenance(self._service, storage_domain)