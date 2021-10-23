def delete(self, path, data=None, headers=None):
    return self.send('DELETE', path, data, headers)