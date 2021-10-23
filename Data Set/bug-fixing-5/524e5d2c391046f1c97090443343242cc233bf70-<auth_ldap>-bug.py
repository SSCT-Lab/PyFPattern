def auth_ldap(self, **kwargs):
    username = kwargs.get('username')
    if (username == None):
        raise AnsibleError('Authentication method ldap requires a username')
    password = kwargs.get('password')
    if (password == None):
        raise AnsibleError('Authentication method ldap requires a password')
    mount_point = kwargs.get('mount_point')
    if (mount_point == None):
        mount_point = 'ldap'
    self.client.auth_ldap(username, password, mount_point)