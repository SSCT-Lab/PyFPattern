@cached_property
def select(self):
    return (self.geom_func_prefix + 'AsText(%s)')