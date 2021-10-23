def provided_password(self):
    if self.want.password:
        return self.password
    if self.want.provider.get('password', None):
        return self.want.provider.get('password')
    if self.module.params.get('password', None):
        return self.module.params.get('password')