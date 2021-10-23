@cached_property
def from_wkb(self):
    if self.is_mysql_5_5:
        return 'GeomFromWKB'
    return 'ST_GeomFromWKB'