def __init__(self, symbol, model_prefix, epoch, data_shape, mean_pixels, batch_size=1, ctx=None):
    self.ctx = ctx
    if (self.ctx is None):
        self.ctx = mx.cpu()
    (load_symbol, args, auxs) = mx.model.load_checkpoint(model_prefix, epoch)
    if (symbol is None):
        symbol = load_symbol
    self.mod = mx.mod.Module(symbol, label_names=None, context=ctx)
    if (not isinstance(data_shape, tuple)):
        data_shape = (data_shape, data_shape)
    self.data_shape = data_shape
    self.mod.bind(data_shapes=[('data', (batch_size, 3, data_shape[0], data_shape[1]))])
    self.mod.set_params(args, auxs)
    self.mean_pixels = mean_pixels