

@deprecation.deprecated(date=None, instructions="tf.py_func is deprecated in TF V2. Instead, there are two\n    options available in V2.\n    - tf.py_function takes a python function which manipulates tf eager\n    tensors instead of numpy arrays. It's easy to convert a tf eager tensor to\n    an ndarray (just call tensor.numpy()) but having access to eager tensors\n    means `tf.py_function`s can use accelerators such as GPUs as well as\n    being differentiable using a gradient tape.\n    - tf.numpy_function maintains the semantics of the deprecated tf.py_func\n    (it is not differentiable, and manipulates numpy arrays). It drops the\n    stateful argument making all functions stateful.\n    ")
@tf_export(v1=['py_func'])
def py_func(func, inp, Tout, stateful=True, name=None):
    return py_func_common(func, inp, Tout, stateful, name=name)
