def _get_qos_id(self):
    if self.param('qos'):
        qoss_service = self._get_dcs_service().service(self._get_dcs_id()).qoss_service()
        return (get_id_by_name(qoss_service, self.param('qos')) if self.param('qos') else None)
    return None