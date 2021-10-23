@property
def hostports_available(self):
    used_ids = list()
    try:
        (rc, self.available_ports) = request((self.url + ('storage-systems/%s/unassociated-host-ports' % self.ssid)), url_password=self.pwd, url_username=self.user, validate_certs=self.certs, headers=HEADERS)
    except:
        err = get_exception()
        self.module.fail_json(msg=('Failed to get unassociated host ports. Array Id [%s]. Error [%s].' % (self.ssid, str(err))))
    if ((len(self.available_ports) > 0) and (len(self.ports) <= len(self.available_ports))):
        for port in self.ports:
            for free_port in self.available_ports:
                if (not (free_port['id'] in used_ids)):
                    used_ids.append(free_port['id'])
                    break
        if ((len(used_ids) != len(self.ports)) and (not self.force_port)):
            self.module.fail_json(msg='There are not enough free host ports with the specified port types to proceed')
        else:
            return True
    else:
        self.module.fail_json(msg='There are no host ports available OR there are not enough unassigned host ports')