def fetchmany(self, size=None):
    if (size is None):
        size = self.arraysize
    return tuple((_rowfactory(r, self.cursor) for r in self.cursor.fetchmany(size)))