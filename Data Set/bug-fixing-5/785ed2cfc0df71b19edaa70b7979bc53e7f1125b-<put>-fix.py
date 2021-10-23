def put(self, path, data=None):
    return self.send('PUT', path, data)