def unattached_pre_action(self, storage_domain):
    dc_name = self.param('data_center')
    if (not dc_name):
        dc_name = self._find_attached_datacenter_name(storage_domain.name)
    self._service = self._attached_sds_service(dc_name)
    self._maintenance(storage_domain)