

def view(g, self, size):
    if (self.type().sizes()[0] == size[0]):
        return g.op('Flatten', self, axis_i=1)
    return g.op('Reshape', self, shape_i=size)
