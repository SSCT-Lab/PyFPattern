

def store_clear(self):
    for key in self.store_keys():
        self.store_delete(key)
    self.store_sync()
