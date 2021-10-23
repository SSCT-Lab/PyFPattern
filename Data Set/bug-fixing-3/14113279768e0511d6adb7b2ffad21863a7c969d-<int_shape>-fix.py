def int_shape(x):
    'Returns the shape of a Keras tensor or a Keras variable as a tuple of\n    integers or None entries.\n\n    # Arguments\n        x: Tensor or variable.\n\n    # Returns\n        A tuple of integers (or None entries).\n    '
    if hasattr(x, '_keras_shape'):
        return x._keras_shape
    else:
        return None