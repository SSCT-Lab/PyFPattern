def get_multi(self, id_list):
    if (len(id_list) == 1):
        id = id_list[0]
        return {
            id: self.get(id),
        }
    rv = {
        
    }
    rows = RowSet()
    for id in id_list:
        rows.add_row_key(id)
        rv[id] = None
    for row in self.connection.read_rows(row_set=rows):
        rv[row.row_key] = self.decode_row(row)
    return rv