@cached_property
def from_wkb(self):
    return (self.geom_func_prefix + 'GeomFromWKB')