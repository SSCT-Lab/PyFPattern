def set(self, id, data, ttl=None):
    data = json_dumps(data)
    row = self.connection.row(id)
    row.delete()
    ttl = (ttl or self.default_ttl)
    if (ttl is None):
        ts = None
    else:
        ts = (timezone.now() + ttl)
        row.set_cell(self.column_family, self.ttl_column, struct.pack('<I', int(ttl.total_seconds())), timestamp=ts)
    flags = 0
    if self.compression:
        flags |= self._FLAG_COMPRESSED
        data = zlib_compress(data)
    if flags:
        row.set_cell(self.column_family, self.flags_column, struct.pack('B', flags), timestamp=ts)
    assert (len(data) <= self.max_size)
    row.set_cell(self.column_family, self.data_column, data, timestamp=ts)
    self.connection.mutate_rows([row])