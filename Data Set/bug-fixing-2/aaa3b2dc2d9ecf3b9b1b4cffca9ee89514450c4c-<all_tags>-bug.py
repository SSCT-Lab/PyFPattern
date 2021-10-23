

def all_tags(self):
    resp = self.send('tags/')
    return resp['tags']
