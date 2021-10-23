def __iter__(self):
    return (_rowfactory(r, self.cursor) for r in self.cursor)