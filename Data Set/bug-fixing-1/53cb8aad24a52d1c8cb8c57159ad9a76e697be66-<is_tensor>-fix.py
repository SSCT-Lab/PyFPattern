

def is_tensor(x):
    'Check whether `x` is of tensor type.\n\n  Check whether an object is a tensor. This check is equivalent to calling\n  `isinstance(x, (tf.Tensor, tf.SparseTensor, tf.Variable))` and also checks\n  if all the component variables of a MirroredVariable or a TowerLocalVariable\n  are tensors.\n\n  Args:\n    x: A python object to check.\n\n  Returns:\n    `True` if `x` is a tensor, `False` if not.\n  '
    return (isinstance(x, ops._TensorLike) or ops.is_dense_tensor_like(x) or (hasattr(x, 'is_tensor_like') and x.is_tensor_like))
