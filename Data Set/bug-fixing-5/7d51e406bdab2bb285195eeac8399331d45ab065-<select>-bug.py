@cached_property
def select(self):
    if self.is_mysql_5_5:
        return 'AsText(%s)'
    return 'ST_AsText(%s)'