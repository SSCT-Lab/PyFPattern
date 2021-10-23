def save(self):
    tmp = (self.filename + '.new')
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(self.cache, f)
    os.rename(tmp, self.filename)