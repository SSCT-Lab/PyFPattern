def _check_and_get(self, arr_dict, ctx):
    if (arr_dict is not None):
        if (ctx is list):
            return list(arr_dict.values())
        if (ctx is None):
            if (len(self._ctx_list) == 1):
                ctx = self._ctx_list[0]
            else:
                ctx = context.current_context()
        ret = arr_dict.get(ctx, None)
        if (ret is not None):
            return ret
        raise RuntimeError(('Parameter %s was not initialized on context %s. It was only initialized on %s.' % (self.name, str(ctx), str(self._ctx_list))))
    if self._deferred_init:
        raise DeferredInitializationError
    raise RuntimeError(('Parameter %s has not been initialized. Note that you should initialize parameters and create Trainer with Block.collect_params() instead of Block.params because the later does not include Parameters of nested child Blocks' % self.name))