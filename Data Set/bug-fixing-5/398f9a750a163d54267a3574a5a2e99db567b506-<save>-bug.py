def save(self):
    tmp = (self.filename + '.new')
    with open(tmp, 'wb') as f:
        json.dump(self.cache, f)
    os.rename(tmp, self.filename)