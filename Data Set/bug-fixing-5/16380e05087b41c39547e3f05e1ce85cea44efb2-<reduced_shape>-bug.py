def reduced_shape(input_shape, axes):
    'Helper function for reduction ops.\n\n  Args:\n    input_shape: 1-D Tensor, the shape of the Tensor being reduced.\n    axes: 1-D Tensor, the reduction axes.\n  Returns:\n    A 1-D Tensor, the output shape as if keepdims were set to True.\n  '
    if context.executing_eagerly():
        input_shape = input_shape.numpy()
        axes = axes.numpy()
        input_shape[axes] = 1
        return input_shape
    input_shape = to_int32(input_shape)
    axes = to_int32(axes)
    input_rank = array_ops.size(input_shape)
    axes = ((axes + input_rank) % input_rank)
    axes_shape = array_ops.shape(axes)
    return gen_data_flow_ops.dynamic_stitch([range(input_rank), axes], [input_shape, array_ops.fill(axes_shape, 1)])