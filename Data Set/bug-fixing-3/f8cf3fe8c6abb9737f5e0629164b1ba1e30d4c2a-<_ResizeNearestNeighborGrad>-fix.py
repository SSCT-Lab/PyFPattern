@ops.RegisterGradient('ResizeNearestNeighbor')
def _ResizeNearestNeighborGrad(op, grad):
    'The derivatives for nearest neighbor resizing.\n\n  Args:\n    op: The ResizeNearestNeighbor op.\n    grad: The tensor representing the gradient w.r.t. the output.\n\n  Returns:\n    The gradients w.r.t. the input and the output.\n  '
    image = op.inputs[0]
    if image.get_shape()[1:3].is_fully_defined():
        image_shape = image.get_shape()[1:3]
    else:
        image_shape = array_ops.shape(image)[1:3]
    grads = gen_image_ops._resize_nearest_neighbor_grad(grad, image_shape, align_corners=op.get_attr('align_corners'))
    return [grads, None]