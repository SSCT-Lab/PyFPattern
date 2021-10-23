def create_thin_volume(self, pool_id, name, size_unit, size, thin_volume_repo_size, thin_volume_max_repo_size, data_assurance_enabled):
    thin_volume_add_req = dict(name=name, poolId=pool_id, sizeUnit=size_unit, virtualSize=size, repositorySize=thin_volume_repo_size, maximumRepositorySize=thin_volume_max_repo_size, dataAssuranceEnabled=data_assurance_enabled)
    self.debug(("creating thin-volume '%s'" % name))
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/thin-volumes' % self.ssid)), data=json.dumps(thin_volume_add_req), headers=self._post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except Exception:
        err = get_exception()
        self.module.fail_json(msg=('Failed to create thin volume.  Volume [%s].  Array Id [%s]. Error[%s].' % (self.name, self.ssid, str(err))))