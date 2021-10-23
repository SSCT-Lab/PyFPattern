

def parallel_forward(self, inputs):
    inputs = tuple([tuple([x.as_in_context(ctx)]) for (x, ctx) in zip(inputs, self.ctx_list)])
    if (len(self.ctx_list) == 1):
        return self(*inputs[0])
    return parallel_apply(self, inputs, sync=True)
