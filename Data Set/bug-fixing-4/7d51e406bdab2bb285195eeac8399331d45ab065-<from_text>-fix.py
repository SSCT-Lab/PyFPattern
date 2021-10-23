@cached_property
def from_text(self):
    return (self.geom_func_prefix + 'GeomFromText')