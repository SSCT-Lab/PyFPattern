def expand_volume(self):
    is_thin = self.volume_detail['thinProvisioned']
    if is_thin:
        self.debug('expanding thin volume')
        thin_volume_expand_req = dict(newVirtualSize=self.size, sizeUnit=self.size_unit)
        try:
            (rc, resp) = request((self.api_url + ('/storage-systems/%s/thin-volumes/%s/expand' % (self.ssid, self.volume_detail['id']))), data=json.dumps(thin_volume_expand_req), headers=self._post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
        except Exception:
            err = get_exception()
            self.module.fail_json(msg=('Failed to expand thin volume.  Volume [%s].  Array Id [%s]. Error[%s].' % (self.name, self.ssid, str(err))))
    else:
        self.debug('expanding volume')
        volume_expand_req = dict(expansionSize=self.size, sizeUnit=self.size_unit)
        try:
            (rc, resp) = request((self.api_url + ('/storage-systems/%s/volumes/%s/expand' % (self.ssid, self.volume_detail['id']))), data=json.dumps(volume_expand_req), headers=self._post_headers, method='POST', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs, timeout=120)
        except Exception:
            err = get_exception()
            self.module.fail_json(msg=('Failed to expand volume.  Volume [%s].  Array Id [%s]. Error[%s].' % (self.name, self.ssid, str(err))))
        self.debug('polling for completion...')
        while True:
            try:
                (rc, resp) = request((self.api_url + ('/storage-systems/%s/volumes/%s/expand' % (self.ssid, self.volume_detail['id']))), method='GET', url_username=self.api_usr, url_password=self.api_pwd, validate_certs=self.validate_certs)
            except Exception:
                err = get_exception()
                self.module.fail_json(msg=('Failed to get volume expansion progress.  Volume [%s].  Array Id [%s]. Error[%s].' % (self.name, self.ssid, str(err))))
            action = resp['action']
            percent_complete = resp['percentComplete']
            self.debug(('expand action %s, %s complete...' % (action, percent_complete)))
            if (action == 'none'):
                self.debug('expand complete')
                break
            else:
                time.sleep(5)