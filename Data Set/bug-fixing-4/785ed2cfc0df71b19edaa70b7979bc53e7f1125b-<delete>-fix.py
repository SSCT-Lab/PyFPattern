def delete(self, path, data=None):
    return self.send('DELETE', path, data)