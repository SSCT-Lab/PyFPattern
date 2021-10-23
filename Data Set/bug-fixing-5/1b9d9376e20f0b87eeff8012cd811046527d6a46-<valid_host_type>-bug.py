@property
def valid_host_type(self):
    try:
        (rc, host_types) = request((self.url + ('storage-systems/%s/host-types' % self.ssid)), url_password=self.pwd, url_username=self.user, validate_certs=self.certs, headers=HEADERS)
    except Exception:
        err = get_exception()
        self.module.fail_json(msg=('Failed to get host types. Array Id [%s]. Error [%s].' % (self.ssid, str(err))))
    try:
        match = filter((lambda host_type: (host_type['index'] == self.host_type_index)), host_types)[0]
        return True
    except IndexError:
        self.module.fail_json(msg=('There is no host type with index %s' % self.host_type_index))