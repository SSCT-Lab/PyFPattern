@property
def sp_drives(self, exclude_hotspares=True):
    if (not self._sp_drives_cached):
        self.debug('fetching drive list...')
        try:
            (rc, resp) = request((self.api_url + ('/storage-systems/%s/drives' % self.ssid)), method='GET', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs)
        except:
            err = get_exception()
            pool_id = self.pool_detail['id']
            self.module.exit_json(msg=('Failed to fetch disk drives. Pool id [%s]. Array id [%s].  Error[%s].' % (pool_id, self.ssid, str(err))))
        sp_id = self.pool_detail['id']
        if exclude_hotspares:
            self._sp_drives_cached = [d for d in resp if ((d['currentVolumeGroupRef'] == sp_id) and (not d['hotSpare']))]
        else:
            self._sp_drives_cached = [d for d in resp if (d['currentVolumeGroupRef'] == sp_id)]
    return self._sp_drives_cached