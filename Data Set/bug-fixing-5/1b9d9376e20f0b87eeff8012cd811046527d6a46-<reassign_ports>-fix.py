def reassign_ports(self, apply=True):
    if (not self.post_body):
        self.post_body = dict(portsToUpdate=dict())
    for port in self.ports:
        if self.port_on_diff_host(port):
            self.post_body['portsToUpdate'].update(dict(portRef=self.other_host['hostPortRef'], hostRef=self.host_obj['id']))
    if apply:
        try:
            (rc, self.host_obj) = request((self.url + ('storage-systems/%s/hosts/%s' % (self.ssid, self.host_obj['id']))), url_username=self.user, url_password=self.pwd, headers=HEADERS, validate_certs=self.certs, method='POST', data=json.dumps(self.post_body))
        except:
            err = get_exception()
            self.module.fail_json(msg=('Failed to reassign host port. Host Id [%s]. Array Id [%s]. Error [%s].' % (self.host_obj['id'], self.ssid, str(err))))