

def update_check(self, entity):
    return (equal(self.param('address'), entity.address) and equal(self.param('path'), entity.path) and equal(self.param('nfs_version'), entity.nfs_version) and equal(self.param('nfs_timeout'), entity.nfs_timeo) and equal(self.param('nfs_retrans'), entity.nfs_retrans) and equal(self.param('mount_options'), entity.mount_options) and equal(self.param('password'), entity.password) and equal(self.param('username'), entity.username) and equal(self.param('port'), entity.port) and equal(self.param('target'), entity.target) and equal(self.param('type'), str(entity.type)) and equal(self.param('vfs_type'), entity.vfs_type))
