def has_permissions_modifications(self):
    sort_key_fetch = operator.itemgetter('vhost')
    return (sorted(self._permissions, key=sort_key_fetch) != sorted(self.permissions, key=sort_key_fetch))