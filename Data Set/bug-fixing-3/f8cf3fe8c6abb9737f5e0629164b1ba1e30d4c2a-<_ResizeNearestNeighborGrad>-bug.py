@ops.RegisterGradient('ResizeNearestNeighbor')
def _ResizeNearestNeighborGrad(op, grad):
    'The derivatives for nearest neighbor resizing.\n\n  Args:\n    op: The ResizeNearestNeighbor op.\n    grad: The tensor representing the gradient w.r.t. the output.\n\n  Returns:\n    The gradients w.r.t. the input and the output.\n  '
    grads = gen_image_ops._resize_nearest_neighbor_grad(grad, op.inputs[0].get_shape()[1:3], align_corners=op.get_attr('align_corners'))
    return [grads, None]