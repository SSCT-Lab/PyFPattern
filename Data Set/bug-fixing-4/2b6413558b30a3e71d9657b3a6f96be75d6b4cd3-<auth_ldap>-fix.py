def auth_ldap(self, **kwargs):
    (username, password, mount_point) = self.check_params(**kwargs)
    if (mount_point is None):
        mount_point = 'ldap'
    self.client.auth_ldap(username, password, mount_point=mount_point)