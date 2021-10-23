def get_storage_pool(self, storage_pool_name):
    self.debug('fetching storage pools')
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/storage-pools' % self.ssid)), headers=dict(Accept='application/json'), url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs)
    except Exception:
        err = get_exception()
        self.module.fail_json(msg=('Failed to obtain list of storage pools.  Array Id [%s]. Error[%s].' % (self.ssid, str(err))))
    self.debug(("searching for storage pool '%s'" % storage_pool_name))
    pool_detail = next(ifilter((lambda a: (a['name'] == storage_pool_name)), resp), None)
    if pool_detail:
        self.debug('found')
    else:
        self.debug('not found')
    return pool_detail