def __init__(self, sym_gen, default_bucket_key=None, logger=logging, context=ctx.cpu(), work_load_list=None, fixed_param_names=None, state_names=None, group2ctxs=None, compression_params=None):
    super(BucketingModule, self).__init__(logger=logger)
    assert (default_bucket_key is not None)
    self._default_bucket_key = default_bucket_key
    self._sym_gen = sym_gen
    (symbol, data_names, label_names) = sym_gen(default_bucket_key)
    data_names = (list(data_names) if (data_names is not None) else [])
    label_names = (list(label_names) if (label_names is not None) else [])
    state_names = (list(state_names) if (state_names is not None) else [])
    fixed_param_names = (list(fixed_param_names) if (fixed_param_names is not None) else [])
    _check_input_names(symbol, data_names, 'data', True)
    _check_input_names(symbol, label_names, 'label', False)
    _check_input_names(symbol, state_names, 'state', True)
    _check_input_names(symbol, fixed_param_names, 'fixed_param', True)
    self._compression_params = compression_params
    self._fixed_param_names = fixed_param_names
    self._state_names = state_names
    self._context = context
    self._work_load_list = work_load_list
    self._group2ctxs = group2ctxs
    self._buckets = {
        
    }
    self._curr_module = None
    self._curr_bucket_key = None
    self._params_dirty = False
    self._monitor = None