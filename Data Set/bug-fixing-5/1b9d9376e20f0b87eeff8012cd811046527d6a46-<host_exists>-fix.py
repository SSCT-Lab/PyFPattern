@property
def host_exists(self):
    try:
        (rc, all_hosts) = request((self.url + ('storage-systems/%s/hosts' % self.ssid)), url_password=self.pwd, url_username=self.user, validate_certs=self.certs, headers=HEADERS)
    except:
        err = get_exception()
        self.module.fail_json(msg=('Failed to determine host existence. Array Id [%s]. Error [%s].' % (self.ssid, str(err))))
    self.all_hosts = all_hosts
    try:
        self.host_obj = filter((lambda host: (host['label'] == self.name)), all_hosts)[0]
        return True
    except IndexError:
        return False