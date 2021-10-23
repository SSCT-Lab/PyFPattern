def remove_host(self):
    try:
        (rc, resp) = request((self.url + ('storage-systems/%s/hosts/%s' % (self.ssid, self.host_obj['id']))), method='DELETE', url_username=self.user, url_password=self.pwd, validate_certs=self.certs)
    except:
        err = get_exception()
        self.module.fail_json(msg=('Failed to remote host.  Host[%s]. Array Id [%s]. Error [%s].' % (self.host_obj['id'], self.ssid, str(err))))