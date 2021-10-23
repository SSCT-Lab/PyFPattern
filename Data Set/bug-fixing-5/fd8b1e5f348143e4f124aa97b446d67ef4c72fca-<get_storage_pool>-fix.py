def get_storage_pool(self, storage_pool_name):
    self.debug('fetching storage pools')
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/storage-pools' % self.ssid)), headers=dict(Accept='application/json'), url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs)
    except Exception:
        err = get_exception()
        rc = err.args[0]
        if ((rc == 404) and (self.state == 'absent')):
            self.module.exit_json(msg=('Storage pool [%s] did not exist.' % self.name))
        else:
            err = get_exception()
            self.module.exit_json(msg=('Failed to get storage pools. Array id [%s].  Error[%s]. State[%s]. RC[%s].' % (self.ssid, str(err), self.state, rc)))
    self.debug(("searching for storage pool '%s'" % storage_pool_name))
    pool_detail = next(select((lambda a: (a['name'] == storage_pool_name)), resp), None)
    if pool_detail:
        found = 'found'
    else:
        found = 'not found'
    self.debug(found)
    return pool_detail