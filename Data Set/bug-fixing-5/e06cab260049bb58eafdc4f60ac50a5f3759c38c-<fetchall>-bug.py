def fetchall(self):
    return tuple((_rowfactory(r, self.cursor) for r in self.cursor.fetchall()))