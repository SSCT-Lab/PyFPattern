def update_reserve_drive_count(self, qty):
    data = dict(reservedDriveCount=qty)
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/storage-pools/%s' % (self.ssid, self.pool_detail['id']))), data=json.dumps(data), headers=self.post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except:
        err = get_exception()
        pool_id = self.pool_detail['id']
        self.module.exit_json(msg=('Failed to update reserve drive count. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))