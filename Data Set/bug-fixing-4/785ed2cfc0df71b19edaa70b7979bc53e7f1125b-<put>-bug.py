def put(self, path, data=None, headers=None):
    return self.send('PUT', path, data, headers)