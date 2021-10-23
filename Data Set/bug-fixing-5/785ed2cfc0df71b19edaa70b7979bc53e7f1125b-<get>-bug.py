def get(self, path, data=None, headers=None):
    return self.send('GET', path, data, headers)