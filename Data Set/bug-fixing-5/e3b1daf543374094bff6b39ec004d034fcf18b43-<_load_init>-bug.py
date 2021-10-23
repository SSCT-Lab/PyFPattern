def _load_init(self, data, ctx):
    '(Re)initializes by loading from data.'
    if self.shape:
        for (self_dim, data_dim) in zip(self.shape, data.shape):
            assert ((self_dim == 0) or (self_dim == data_dim)), ("Failed loading Parameter '%s' from saved params: shape incompatible expacted %s vs saved %s" % (self.name, str(self.shape), str(data.shape)))
        self.shape = tuple(((i if (i != 0) else j) for (i, j) in zip(self.shape, data.shape)))
    if self.dtype:
        assert (np.dtype(self.dtype).type == data.dtype), ("Failed loading Parameter '%s' from saved params: dtype incompatible expacted %s vs saved %s" % (self.name, str(self.dtype), str(data.dtype)))
    if isinstance(ctx, Context):
        ctx = [ctx]
    if (self._data is None):
        if self._deferred_init:
            assert ((ctx is None) or (set(ctx) == set(self._deferred_init[1]))), ("Failed to load Parameter '%s' on %s because it was previous initialized on %s." % (self.name, str(ctx), str(self.list_ctx())))
            ctx = self._deferred_init[1]
        elif (ctx is None):
            ctx = [cpu()]
        self._init_impl(data, ctx)
    else:
        assert ((ctx is None) or (set(ctx) == set(self.list_ctx()))), ("Failed to load Parameter '%s' on %s because it was previous initialized on %s." % (self.name, str(ctx), str(self.list_ctx())))
        self.set_data(data)
    self._deferred_init = ()