def post(self, path, data=None, headers=None):
    return self.send('POST', path, data, headers)