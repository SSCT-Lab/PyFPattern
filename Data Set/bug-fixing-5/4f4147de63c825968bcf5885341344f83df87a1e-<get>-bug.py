def get(self, id):
    row = self.connection.read_row(id)
    if (row is None):
        return None
    columns = row.cells[self.column_family]
    try:
        cell = columns[self.data_column][0]
    except KeyError:
        return None
    if (self.ttl_column in columns):
        if (cell.timestamp < timezone.now()):
            return None
    data = cell.value
    flags = 0
    if (self.flags_column in columns):
        flags = struct.unpack('B', columns[self.flags_column][0].value)[0]
    if (flags & self._FLAG_COMPRESSED):
        data = zlib_decompress(data)
    return json_loads(data)