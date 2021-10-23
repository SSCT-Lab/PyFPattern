def create_volume(self, pool_id, name, size_unit, size, segment_size_kb, data_assurance_enabled):
    volume_add_req = dict(name=name, poolId=pool_id, sizeUnit=size_unit, size=size, segSize=segment_size_kb, dataAssuranceEnabled=data_assurance_enabled)
    self.debug(("creating volume '%s'" % name))
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/volumes' % self.ssid)), data=json.dumps(volume_add_req), headers=HEADERS, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except Exception:
        err = get_exception()
        self.module.fail_json(msg=('Failed to create volume.  Volume [%s].  Array Id [%s]. Error[%s].' % (self.name, self.ssid, str(err))))