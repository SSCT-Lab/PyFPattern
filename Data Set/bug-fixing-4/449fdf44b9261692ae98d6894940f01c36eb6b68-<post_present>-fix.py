def post_present(self, entity_id):
    if self.param('storage'):
        (sd, sd_service) = self._get_storage_domain_service()
        if (entity_id not in [sd_conn.id for sd_conn in self._connection.follow_link(sd.storage_connections)]):
            scs_service = sd_service.storage_connections_service()
            if (not self._module.check_mode):
                scs_service.add(connection=otypes.StorageConnection(id=entity_id))
            self.changed = True