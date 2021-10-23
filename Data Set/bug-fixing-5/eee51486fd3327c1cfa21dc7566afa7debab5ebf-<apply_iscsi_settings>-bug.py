def apply_iscsi_settings(self):
    'Update the iSCSI target alias and CHAP settings'
    update = False
    target = self.target
    body = dict()
    if ((self.name is not None) and (self.name != target['alias'])):
        update = True
        body['alias'] = self.name
    if (self.chap_secret is not None):
        update = True
        body.update(dict(enableChapAuthentication=True, chapSecret=self.chap_secret))
    elif target['chap']:
        update = True
        body.update(dict(enableChapAuthentication=False))
    self._logger.info(pformat(body))
    if (update and (not self.check_mode)):
        try:
            request((self.url + ('storage-systems/%s/iscsi/target-settings' % self.ssid)), method='POST', data=json.dumps(body), headers=HEADERS, **self.creds)
        except Exception as err:
            self.module.fail_json(msg=('Failed to update the iSCSI target settings. Array Id [%s]. Error [%s].' % (self.ssid, to_native(err))))
    return update