def set(self, id, data, ttl=None):
    row = self.encode_row(id, data, ttl)
    row.commit()