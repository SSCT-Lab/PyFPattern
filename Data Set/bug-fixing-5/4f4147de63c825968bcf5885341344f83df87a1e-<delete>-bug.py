def delete(self, id):
    if self.skip_deletes:
        return
    row = self.connection.row(id)
    row.delete()
    self.connection.mutate_rows([row])