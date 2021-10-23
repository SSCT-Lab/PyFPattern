def _attached_sds_service(self, dc_name):
    dcs_service = self._connection.system_service().data_centers_service()
    dc = search_by_name(dcs_service, dc_name)
    if (dc is None):
        dc = get_entity(dcs_service.service(dc_name))
        if (dc is None):
            return None
    dc_service = dcs_service.data_center_service(dc.id)
    return dc_service.storage_domains_service()