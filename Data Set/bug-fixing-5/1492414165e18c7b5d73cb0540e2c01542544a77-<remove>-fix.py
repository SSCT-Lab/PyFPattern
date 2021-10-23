def remove(self):
    if self.module.check_mode:
        return True
    if (self.want.peer_hostname is None):
        self.want.update({
            'peer_hostname': self.want.peer_server,
        })
    self.remove_from_device()
    if self.exists():
        raise F5ModuleError('Failed to remove the trusted peer.')
    return True