@tf_export('linalg.logdet')
def logdet(matrix, name=None):
    'Computes log of the determinant of a hermitian positive definite matrix.\n\n  ```python\n  # Compute the determinant of a matrix while reducing the chance of over- or\n  underflow:\n  A = ... # shape 10 x 10\n  det = tf.exp(tf.linalg.logdet(A))  # scalar\n  ```\n\n  Args:\n    matrix:  A `Tensor`. Must be `float16`, `float32`, `float64`, `complex64`,\n      or `complex128` with shape `[..., M, M]`.\n    name:  A name to give this `Op`.  Defaults to `logdet`.\n\n  Returns:\n    The natural log of the determinant of `matrix`.\n\n  @compatibility(numpy)\n  Equivalent to numpy.linalg.slogdet, although no sign is returned since only\n  hermitian positive definite matrices are supported.\n  @end_compatibility\n  '
    with ops.name_scope(name, 'logdet', [matrix]):
        chol = gen_linalg_ops.cholesky(matrix)
        return (2.0 * math_ops.reduce_sum(math_ops.log(math_ops.real(array_ops.matrix_diag_part(chol))), axis=[(- 1)]))