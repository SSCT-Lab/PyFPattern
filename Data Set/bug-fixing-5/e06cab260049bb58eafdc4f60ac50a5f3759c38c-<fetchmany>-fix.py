def fetchmany(self, size=None):
    if (size is None):
        size = self.arraysize
    return tuple(self.cursor.fetchmany(size))