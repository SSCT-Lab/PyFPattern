def delete_volume(self):
    self.debug(("deleting volume '%s'" % self.volume_detail['name']))
    try:
        (rc, resp) = request((self.api_url + ('/storage-systems/%s/%s/%s' % (self.ssid, self.volume_resource_name, self.volume_detail['id']))), method='DELETE', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
    except Exception:
        err = get_exception()
        self.module.fail_json(msg=('Failed to delete volume.  Volume [%s].  Array Id [%s]. Error[%s].' % (self.name, self.ssid, str(err))))