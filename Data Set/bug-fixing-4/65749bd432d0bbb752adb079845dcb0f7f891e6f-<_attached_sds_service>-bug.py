def _attached_sds_service(self):
    dcs_service = self._connection.system_service().data_centers_service()
    dc = search_by_name(dcs_service, self._module.params['data_center'])
    if (dc is None):
        dc = dcs_service.service(self._module.params['data_center']).get()
        if (dc is None):
            return
    dc_service = dcs_service.data_center_service(dc.id)
    return dc_service.storage_domains_service()