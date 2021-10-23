def post(self, path, data=None):
    return self.send('POST', path, data)