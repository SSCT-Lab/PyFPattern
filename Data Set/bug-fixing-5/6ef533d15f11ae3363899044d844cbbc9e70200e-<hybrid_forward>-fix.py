def hybrid_forward(self, F, x):
    return ((x * self.std.reshape(shape=(3, 1, 1))) + self.mean.reshape(shape=(3, 1, 1)))