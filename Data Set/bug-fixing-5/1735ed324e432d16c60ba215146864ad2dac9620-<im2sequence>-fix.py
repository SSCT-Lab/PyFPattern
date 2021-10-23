def im2sequence(input, filter_size=1, stride=1, padding=0, input_image_size=None, out_stride=1, name=None):
    "\n    Extracts image patches from the input tensor to form a tensor of shape\n    {input.batch_size * output_height * output_width, filter_size_H *\n    filter_size_W * input.channels} which is similar with im2col.\n    This op use filter / kernel to scan images and convert these images to\n    sequences. After expanding, the number of time step are\n    output_height * output_width for an image, in which output_height and\n    output_width are calculated by below equation:\n\n    .. math::\n\n        output\\_size = 1 +             (2 * padding + img\\_size - block\\_size + stride - 1) / stride\n\n    And the dimension of each time step is block_y * block_x * input.channels.\n\n    Args:\n        input (Variable): The input should be a tensor in NCHW format.\n\n        filter_size(int|tuple|None): The filter size. If filter_size is a tuple,\n            it must contain two integers, (filter_size_H, filter_size_W).\n            Otherwise, the filter will be a square.\n\n        stride(int|tuple): The stride size. If stride is a tuple, it must\n            contain two integers, (stride_H, stride_W). Otherwise, the\n            stride_H = stride_W = stride. Default: stride = 1.\n\n        padding(int|tuple): The padding size. If padding is a tuple, it can\n            contain two integers like (padding_H, padding_W) which means\n            padding_up = padding_down = padding_H and\n            padding_left = padding_right = padding_W. Or it can use\n            (padding_up, padding_left, padding_down, padding_right) to indicate\n            paddings of four direction. Otherwise, a scalar padding means\n            padding_up = padding_down = padding_left = padding_right = padding\n            Default: padding = 0.\n\n        input_image_size(Variable): the input contains image real size.It's dim\n            is [batchsize, 2]. It is dispensable.It is just for batch inference.\n\n        out_stride(int|tuple): The scaling of image through CNN. It is\n            dispensable. It is valid only when input_image_size is not null.\n            If out_stride is tuple,  it must contain two intergers,\n            (out_stride_H, out_stride_W). Otherwise,\n            the out_stride_H = out_stride_W = out_stride.\n\n        name (int): The name of this layer. It is optional.\n\n    Returns:\n        output: The output is a LoDTensor with shape\n        {input.batch_size * output_height * output_width,\n        filter_size_H * filter_size_W * input.channels}.\n        If we regard output as a matrix, each row of this matrix is\n        a step of a sequence.\n\n    Examples:\n\n        .. code-block:: text\n\n            Given:\n\n            x = [[[[ 6.  2.  1.]\n                   [ 8.  3.  5.]\n                   [ 0.  2.  6.]]\n\n                  [[ 2.  4.  4.]\n                   [ 6.  3.  0.]\n                   [ 6.  4.  7.]]]\n\n                 [[[ 6.  7.  1.]\n                   [ 5.  7.  9.]\n                   [ 2.  4.  8.]]\n\n                  [[ 1.  2.  1.]\n                   [ 1.  3.  5.]\n                   [ 9.  0.  8.]]]]\n\n            x.dims = {2, 2, 3, 3}\n\n            And:\n\n            filter = [2, 2]\n            stride = [1, 1]\n            padding = [0, 0]\n\n            Then:\n\n            output.data = [[ 6.  2.  8.  3.  2.  4.  6.  3.]\n                           [ 2.  1.  3.  5.  4.  4.  3.  0.]\n                           [ 8.  3.  0.  2.  6.  3.  6.  4.]\n                           [ 3.  5.  2.  6.  3.  0.  4.  7.]\n                           [ 6.  7.  5.  7.  1.  2.  1.  3.]\n                           [ 7.  1.  7.  9.  2.  1.  3.  5.]\n                           [ 5.  7.  2.  4.  1.  3.  9.  0.]\n                           [ 7.  9.  4.  8.  3.  5.  0.  8.]]\n\n            output.dims = {8, 8}\n\n            output.lod = [[4, 4]]\n\n    Examples:\n\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n            data = fluid.layers.data(name='data', shape=[3, 32, 32],\n                                     dtype='float32')\n            output = fluid.layers.im2sequence(\n                input=data, stride=[1, 1], filter_size=[2, 2])\n\n\n    "
    assert (not in_dygraph_mode()), 'sequence layer is not supported in dygraph mode yet.'
    if isinstance(filter_size, int):
        filter_size = [filter_size, filter_size]
    if isinstance(stride, int):
        stride = [stride, stride]
    if isinstance(padding, int):
        padding = [padding, padding]
    if (len(padding) == 2):
        padding.append(padding[0])
        padding.append(padding[1])
    inputs = {
        'X': input,
    }
    attrs = {
        'kernels': filter_size,
        'strides': stride,
        'paddings': padding,
    }
    if input_image_size:
        if isinstance(out_stride, int):
            out_stride = [out_stride, out_stride]
        inputs['Y'] = input_image_size
        attrs['out_stride'] = out_stride
    helper = LayerHelper('im2sequence', **locals())
    out = helper.create_variable_for_type_inference(dtype=helper.input_dtype())
    helper.append_op(type='im2sequence', inputs=inputs, outputs={
        'Out': out,
    }, attrs=attrs)
    return out