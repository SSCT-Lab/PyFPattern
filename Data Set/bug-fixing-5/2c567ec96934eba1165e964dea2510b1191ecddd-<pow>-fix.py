@tf_export('pow')
def pow(x, y, name=None):
    'Computes the power of one value to another.\n\n  Given a tensor `x` and a tensor `y`, this operation computes \\\\(x^y\\\\) for\n  corresponding elements in `x` and `y`. For example:\n\n  ```python\n  x = tf.constant([[2, 2], [3, 3]])\n  y = tf.constant([[8, 16], [2, 3]])\n  tf.pow(x, y)  # [[256, 65536], [9, 27]]\n  ```\n\n  Args:\n    x: A `Tensor` of type `float16`, `float32`, `float64`, `int32`, `int64`,\n     `complex64`, or `complex128`.\n    y: A `Tensor` of type `float16`, `float32`, `float64`, `int32`, `int64`,\n     `complex64`, or `complex128`.\n    name: A name for the operation (optional).\n\n  Returns:\n    A `Tensor`.\n  '
    with ops.name_scope(name, 'Pow', [x]) as name:
        return gen_math_ops._pow(x, y, name=name)