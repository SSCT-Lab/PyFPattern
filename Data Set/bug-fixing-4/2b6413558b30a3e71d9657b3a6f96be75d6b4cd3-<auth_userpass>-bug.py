def auth_userpass(self, **kwargs):
    (username, password, mount_point) = self.check_params(**kwargs)
    if (mount_point is None):
        mount_point = 'userpass'
    self.client.auth_userpass(username, password, mount_point)