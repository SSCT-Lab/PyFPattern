def __get_network_filter_id(self):
    nf_service = self._connection.system_service().network_filters_service()
    return get_id_by_name(nf_service, self.param('network_filter'))