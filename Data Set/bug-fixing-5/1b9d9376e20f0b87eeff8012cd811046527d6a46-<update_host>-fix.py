def update_host(self):
    if self.ports:
        if self.hostports_available:
            if (self.force_port_update is True):
                self.reassign_ports(apply=False)
                self.ports = [port for port in self.ports if (not self.port_on_diff_host(port))]
            self.post_body['ports'] = self.ports
    if self.group:
        self.post_body['groupId'] = self.group_id
    self.post_body['hostType'] = dict(index=self.host_type_index)
    try:
        (rc, self.host_obj) = request((self.url + ('storage-systems/%s/hosts/%s' % (self.ssid, self.host_obj['id']))), url_username=self.user, url_password=self.pwd, headers=HEADERS, validate_certs=self.certs, method='POST', data=json.dumps(self.post_body))
    except:
        err = get_exception()
        self.module.fail_json(msg=('Failed to update host. Array Id [%s]. Error [%s].' % (self.ssid, str(err))))
    self.module.exit_json(changed=True, **self.host_obj)