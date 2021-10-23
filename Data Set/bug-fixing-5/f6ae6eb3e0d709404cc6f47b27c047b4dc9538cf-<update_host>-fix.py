def update_host(self):
    self._logger.info('Beginning the update for host=%s.', self.name)
    if self.ports:
        self.assigned_host_ports(apply_unassigning=True)
        self.post_body['portsToUpdate'] = self.portsForUpdate
        self.post_body['ports'] = self.newPorts
        self._logger.info('Requested ports: %s', pformat(self.ports))
    else:
        self._logger.info('No host ports were defined.')
    if self.group:
        self.post_body['groupId'] = self.group_id()
    self.post_body['hostType'] = dict(index=self.host_type_index)
    api = (self.url + ('storage-systems/%s/hosts/%s' % (self.ssid, self.host_obj['id'])))
    self._logger.info('POST => url=%s, body=%s.', api, pformat(self.post_body))
    if (not self.check_mode):
        try:
            (rc, self.host_obj) = request(api, url_username=self.user, url_password=self.pwd, headers=HEADERS, validate_certs=self.certs, method='POST', data=json.dumps(self.post_body))
        except Exception as err:
            self.module.fail_json(msg=('Failed to update host. Array Id [%s]. Error [%s].' % (self.ssid, to_native(err))))
    payload = self.build_success_payload(self.host_obj)
    self.module.exit_json(changed=True, **payload)