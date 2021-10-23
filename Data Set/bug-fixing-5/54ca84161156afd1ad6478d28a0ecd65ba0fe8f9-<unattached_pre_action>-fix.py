def unattached_pre_action(self, storage_domain):
    dc_name = self._module.params['data_center']
    self._service = self._attached_sds_service(storage_domain, dc_name)
    self._maintenance(self._service, storage_domain)