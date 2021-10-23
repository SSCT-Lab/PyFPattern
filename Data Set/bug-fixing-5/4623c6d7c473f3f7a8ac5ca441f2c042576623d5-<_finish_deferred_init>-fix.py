def _finish_deferred_init(self, hybrid, *args):
    try:
        self.infer_shape(*args)
    except Exception as e:
        error_msg = 'Deferred initialization failed because shape cannot be inferred \n {}'.format(e)
        raise ValueError(error_msg)
    if hybrid:
        for (is_arg, i) in self._cached_op_args:
            if (not is_arg):
                i._finish_deferred_init()
    else:
        for (_, i) in self.params.items():
            i._finish_deferred_init()