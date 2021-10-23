def create_storage_pool(self):
    self.debug('creating storage pool...')
    sp_add_req = dict(raidLevel=self.raid_level, diskDriveIds=self.disk_ids, name=self.name)
    if self.erase_secured_drives:
        sp_add_req['eraseSecuredDrives'] = self.erase_secured_drives
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/storage-pools' % self.ssid)), data=json.dumps(sp_add_req), headers=self.post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except:
        err = get_exception()
        pool_id = self.pool_detail['id']
        self.module.exit_json(msg=('Failed to create storage pool. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))
    self.pool_detail = self.get_storage_pool(self.name)
    if self.secure_pool:
        secure_pool_data = dict(securePool=True)
        try:
            (retc, r) = request((self.api_url + ('/storage-systems/%s/storage-pools/%s' % (self.ssid, self.pool_detail['id']))), data=json.dumps(secure_pool_data), headers=self.post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120, ignore_errors=True)
        except:
            err = get_exception()
            pool_id = self.pool_detail['id']
            self.module.exit_json(msg=('Failed to update storage pool. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))