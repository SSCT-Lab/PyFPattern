def create_host(self):
    post_body = dict(name=self.name, host_type=dict(index=self.host_type_index), groupId=self.group_id, ports=self.ports)
    if self.ports:
        if self.hostports_available:
            post_body.update(ports=self.ports)
        elif (not self.force_port):
            self.module.fail_json(msg='You supplied ports that are already in use. Supply force_port to True if you wish to reassign the ports')
    if (not self.host_exists):
        try:
            (rc, create_resp) = request((self.url + ('storage-systems/%s/hosts' % self.ssid)), method='POST', url_username=self.user, url_password=self.pwd, validate_certs=self.certs, data=json.dumps(post_body), headers=HEADERS)
        except Exception as err:
            self.module.fail_json(msg=('Failed to create host. Array Id [%s]. Error [%s].' % (self.ssid, to_native(err))))
    else:
        self.module.exit_json(changed=False, msg=('Host already exists. Id [%s]. Host [%s].' % (self.ssid, self.name)))
    self.host_obj = create_resp
    if (self.ports and self.force_port):
        self.reassign_ports()
    self.module.exit_json(changed=True, **self.host_obj)