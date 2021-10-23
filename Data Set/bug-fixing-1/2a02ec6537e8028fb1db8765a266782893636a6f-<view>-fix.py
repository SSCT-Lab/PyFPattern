

def view(g, self, size):
    self_sizes = self.type().sizes()
    if (self_sizes and (len(size) == 2) and (self_sizes[0] == size[0])):
        return g.op('Flatten', self, axis_i=1)
    shape = g.op('Constant', value_t=torch.LongTensor(size))
    return g.op('Reshape', self, shape)
