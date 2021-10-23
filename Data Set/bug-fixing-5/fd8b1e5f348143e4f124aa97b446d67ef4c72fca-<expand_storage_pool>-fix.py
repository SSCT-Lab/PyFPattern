def expand_storage_pool(self):
    drives_to_add = self.get_expansion_candidate_drives()
    self.debug(('adding %s drives to storage pool...' % len(drives_to_add)))
    sp_expand_req = dict(drives=drives_to_add)
    try:
        request((self.api_url + ('/storage-systems/%s/storage-pools/%s/expand' % (self.ssid, self.pool_detail['id']))), data=json.dumps(sp_expand_req), headers=self.post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except:
        err = get_exception()
        pool_id = self.pool_detail['id']
        self.module.exit_json(msg=('Failed to add drives to storage pool. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))