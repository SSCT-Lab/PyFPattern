def reduce_drives(self, drive_list):
    if all(((drive in drive_list) for drive in self.sp_drives)):
        pass
    else:
        self.module.fail_json(msg='One of the drives you wish to remove does not currently exist in the storage pool you specified')
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/storage-pools/%s/reduction' % (self.ssid, self.pool_detail['id']))), data=json.dumps(drive_list), headers=self.post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except:
        err = get_exception()
        pool_id = self.pool_detail['id']
        self.module.exit_json(msg=('Failed to remove drives from storage pool. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))