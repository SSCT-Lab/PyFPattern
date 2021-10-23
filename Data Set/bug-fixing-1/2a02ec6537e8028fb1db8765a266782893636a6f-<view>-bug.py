

def view(g, self, size):
    if ((self.type().sizes()[0] == size[0]) and (len(size) == 2)):
        return g.op('Flatten', self, axis_i=1)
    shape = g.op('Constant', value_t=torch.LongTensor(size))
    return g.op('Reshape', self, shape)
