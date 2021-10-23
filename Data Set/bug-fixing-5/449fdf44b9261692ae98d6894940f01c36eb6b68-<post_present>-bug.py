def post_present(self, entity_id):
    if self.param('storage'):
        sds_service = self._connection.system_service().storage_domains_service()
        sd = search_by_name(sds_service, self.param('storage'))
        if (sd is None):
            raise Exception(("Storage '%s' was not found." % self.param('storage')))
        if (entity_id not in [sd_conn.id for sd_conn in self._connection.follow_link(sd.storage_connections)]):
            scs_service = sds_service.storage_domain_service(sd.id).storage_connections_service()
            if (not self._module.check_mode):
                scs_service.add(connection=otypes.StorageConnection(id=entity_id))
            self.changed = True