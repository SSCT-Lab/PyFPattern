def _finish_deferred_init(self, hybrid, *args):
    self.infer_shape(*args)
    if hybrid:
        for (is_arg, i) in self._cached_op_args:
            if (not is_arg):
                i._finish_deferred_init()
    else:
        for (_, i) in self.params.items():
            i._finish_deferred_init()