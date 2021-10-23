def _login(self, storage_type, storage):
    if (storage_type == 'iscsi'):
        hosts_service = self._connection.system_service().hosts_service()
        host_id = get_id_by_name(hosts_service, self._module.params['host'])
        hosts_service.host_service(host_id).iscsi_login(iscsi=otypes.IscsiDetails(username=storage.get('username'), password=storage.get('password'), address=storage.get('address'), target=storage.get('target')))