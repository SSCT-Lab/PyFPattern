def get_volume(self, volume_name):
    self.debug('fetching volumes')
    try:
        (rc, volumes) = request((self.api_url + ('/storage-systems/%s/volumes' % self.ssid)), headers=dict(Accept='application/json'), url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs)
    except Exception:
        err = get_exception()
        self.module.fail_json(msg=('Failed to obtain list of standard/thick volumes.  Array Id [%s]. Error[%s].' % (self.ssid, str(err))))
    try:
        self.debug('fetching thin-volumes')
        (rc, thinvols) = request((self.api_url + ('/storage-systems/%s/thin-volumes' % self.ssid)), headers=dict(Accept='application/json'), url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs)
    except Exception:
        err = get_exception()
        self.module.fail_json(msg=('Failed to obtain list of thin volumes.  Array Id [%s]. Error[%s].' % (self.ssid, str(err))))
    volumes.extend(thinvols)
    self.debug(("searching for volume '%s'" % volume_name))
    volume_detail = next(ifilter((lambda a: (a['name'] == volume_name)), volumes), None)
    if volume_detail:
        self.debug('found')
    else:
        self.debug('not found')
    return volume_detail