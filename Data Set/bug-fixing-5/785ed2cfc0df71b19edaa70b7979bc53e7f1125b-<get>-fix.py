def get(self, path, data=None):
    return self.send('GET', path, data)