def create(self):
    self._set_changed_options()
    if (self.want.peer_user is None):
        self.want.update({
            'peer_user': self.provided_username(),
        })
    if (self.want.peer_password is None):
        self.want.update({
            'peer_password': self.provided_password(),
        })
    if (self.want.peer_hostname is None):
        self.want.update({
            'peer_hostname': self.want.peer_server,
        })
    if self.module.check_mode:
        return True
    self.create_on_device()
    return True