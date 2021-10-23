

def _compute_dx_and_dy(x, y, y_shape):
    'Returns a node to compute gradient of x wrt y.'
    with x.graph.as_default():
        dy_orig = constant_op.constant(1.0, shape=y_shape, dtype=y.dtype)
        dy = array_ops.identity(dy_orig)
    grads = gradients.gradients(y, x, dy)
    assert (len(grads) == 1)
    return (grads[0], dy_orig)
