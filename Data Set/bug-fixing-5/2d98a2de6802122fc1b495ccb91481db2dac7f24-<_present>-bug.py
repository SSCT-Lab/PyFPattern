def _present(self, path, value):
    if self.exists(path):
        (current_value, zstat) = self.zk.get(path)
        if (value != current_value):
            self.zk.set(path, value)
            return (True, {
                'changed': True,
                'msg': 'Updated the znode value.',
                'znode': path,
                'value': value,
            })
        else:
            return (True, {
                'changed': False,
                'msg': 'No changes were necessary.',
                'znode': path,
                'value': value,
            })
    else:
        self.zk.create(path, value, makepath=True)
        return (True, {
            'changed': True,
            'msg': 'Created a new znode.',
            'znode': path,
            'value': value,
        })