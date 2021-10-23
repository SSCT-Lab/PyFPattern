def delete_multi(self, id_list):
    if self.skip_deletes:
        return
    if (len(id_list) == 1):
        self.delete(id_list[0])
        return
    rows = []
    for id in id_list:
        row = self.connection.row(id)
        row.delete()
        rows.append(row)
    self.connection.mutate_rows(rows)