@tf_export('round')
def round(x, name=None):
    'Rounds the values of a tensor to the nearest integer, element-wise.\n\n  Rounds half to even.  Also known as bankers rounding. If you want to round\n  according to the current system rounding mode use tf::cint.\n  For example:\n\n  ```python\n  x = tf.constant([0.9, 2.5, 2.3, 1.5, -4.5])\n  tf.round(x)  # [ 1.0, 2.0, 2.0, 2.0, -4.0 ]\n  ```\n\n  Args:\n    x: A `Tensor` of type `float32` or `float64`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor` of same shape and type as `x`.\n  '
    x = ops.convert_to_tensor(x, name='x')
    if x.dtype.is_integer:
        return x
    else:
        return gen_math_ops.round(x, name=name)