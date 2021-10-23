def update_volume_properties(self):
    update_volume_req = dict()
    if self.volume_ssdcache_setting_changed:
        update_volume_req['flashCache'] = self.ssd_cache_enabled
    self.debug('updating volume properties...')
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/%s/%s/' % (self.ssid, self.volume_resource_name, self.volume_detail['id']))), data=json.dumps(update_volume_req), headers=self._post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except Exception:
        err = get_exception()
        self.module.fail_json(msg=('Failed to update volume properties.  Volume [%s].  Array Id [%s]. Error[%s].' % (self.name, self.ssid, str(err))))