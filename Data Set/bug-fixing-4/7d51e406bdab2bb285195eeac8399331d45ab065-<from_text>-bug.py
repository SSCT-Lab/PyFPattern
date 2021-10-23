@cached_property
def from_text(self):
    if self.is_mysql_5_5:
        return 'GeomFromText'
    return 'ST_GeomFromText'