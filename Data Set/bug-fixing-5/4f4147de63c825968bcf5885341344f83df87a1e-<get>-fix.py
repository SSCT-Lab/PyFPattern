def get(self, id):
    return self.decode_row(self.connection.read_row(id))