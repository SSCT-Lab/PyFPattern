@property
def group_id(self):
    if self.group:
        try:
            (rc, all_groups) = request((self.url + ('storage-systems/%s/host-groups' % self.ssid)), url_password=self.pwd, url_username=self.user, validate_certs=self.certs, headers=HEADERS)
        except:
            err = get_exception()
            self.module.fail_json(msg=('Failed to get host groups. Array Id [%s]. Error [%s].' % (self.ssid, str(err))))
        try:
            group_obj = filter((lambda group: (group['name'] == self.group)), all_groups)[0]
            return group_obj['id']
        except IndexError:
            self.module.fail_json(msg=('No group with the name: %s exists' % self.group))
    else:
        return '0000000000000000000000000000000000000000'