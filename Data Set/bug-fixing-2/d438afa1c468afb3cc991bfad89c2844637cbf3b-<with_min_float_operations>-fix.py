

def with_min_float_operations(self, min_float_ops):
    "Only show profiler nodes consuming no less than 'min_float_ops'.\n\n    Please see https://github.com/tensorflow/tensorflow/tree/master/tensorflow/core/profiler/g3doc/profile_model_architecture.md\n    on the caveats of calculating float operations.\n\n    Args:\n      min_float_ops: Only show profiler nodes with float operations\n          no less than this.\n    Returns:\n      self\n    "
    self._options['min_float_ops'] = min_float_ops
    return self
