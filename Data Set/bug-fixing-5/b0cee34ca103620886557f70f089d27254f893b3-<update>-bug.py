def update(self):
    'Execute the changes the require changes on the storage array.'
    self.update_mapping_info()
    (target_match, lun_reference) = self.get_lun_mapping()
    update = ((self.state and (not target_match)) or ((not self.state) and target_match))
    if (update and (not self.check_mode)):
        try:
            if self.state:
                body = dict()
                target = (None if (not self.target) else self.mapping_info['target_by_name'][self.target])
                if target:
                    body.update(dict(targetId=target))
                if lun_reference:
                    (rc, response) = request((self.url + ('storage-systems/%s/volume-mappings/%s/move' % (self.ssid, lun_reference))), method='POST', data=json.dumps(body), headers=HEADERS, **self.creds)
                else:
                    body.update(dict(mappableObjectId=self.mapping_info['volume_by_name'][self.volume]))
                    (rc, response) = request((self.url + ('storage-systems/%s/volume-mappings' % self.ssid)), method='POST', data=json.dumps(body), headers=HEADERS, **self.creds)
            else:
                (rc, response) = request((self.url + ('storage-systems/%s/volume-mappings/%s' % (self.ssid, lun_reference))), method='DELETE', headers=HEADERS, **self.creds)
        except Exception as error:
            self.module.fail_json(msg=('Failed to update storage array lun mapping. Id [%s]. Error [%s]' % (self.ssid, to_native(error))))
    self.module.exit_json(msg='Lun mapping is complete.', changed=update)