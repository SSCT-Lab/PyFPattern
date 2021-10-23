def image_resize(input, out_shape=None, scale=None, name=None, resample='BILINEAR', actual_shape=None, align_corners=True, align_mode=1):
    '\n    **Resize a Batch of Images**\n\n    The input must be a tensor of the shape (num_batches, channels, in_h, in_w),\n    and the resizing only applies on the last two dimensions(hight and width).\n\n    Supporting resample methods:\n\n        \'BILINEAR\' : Bilinear interpolation\n\n        \'NEAREST\' : Nearest neighbor interpolation\n\n    Nearest neighbor interpolation is to perform nearest neighbor interpolation\n    in both the 3rd dimention(in height direction) and the 4th dimention(in width \n    direction) on input tensor.\n            \n    Bilinear interpolation is an extension of linear interpolation for \n    interpolating functions of two variables (e.g. H-direction and \n    W-direction in this op) on a rectilinear 2D grid. The key idea is \n    to perform linear interpolation first in one direction, and then \n    again in the other direction.\n\n    Align_corners and align_mode are optinal parameters,the calculation method \n    of interpolation can be selected by them.\n\n    Example:\n\n    .. code-block:: text\n\n        For scale:\n          \n            if align_corners = True && out_size > 1 :\n\n              scale_factor = (in_size-1.0)/(out_size-1.0)\n            \n            else:\n              \n              scale_factor = float(in_size/out_size)\n            \n          \n        Nearest neighbor interpolation:\n          \n          if:\n              align_corners = False\n\n              input : (N,C,H_in,W_in)\n              output: (N,C,H_out,W_out) where:\n\n              H_out = floor (H_{in} * scale_{factor})\n              W_out = floor (W_{in} * scale_{factor})\n\n          else:\n              align_corners = True\n\n              input : (N,C,H_in,W_in)\n              output: (N,C,H_out,W_out) where:\n\n              H_out = round(H_{in} * scale_{factor})\n              W_out = round(W_{in} * scale_{factor})\n\n        Bilinear interpolation:\n\n          if:\n              align_corners = False , align_mode = 0\n              \n              input : (N,C,H_in,W_in)\n              output: (N,C,H_out,W_out) where:\n              \n              H_out = (H_{in}+0.5) * scale_{factor} - 0.5\n              W_out = (W_{in}+0.5) * scale_{factor} - 0.5\n\n          else:\n           \n              input : (N,C,H_in,W_in)\n              output: (N,C,H_out,W_out) where:\n\n              H_out = H_{in} * scale_{factor}\n              W_out = W_{in} * scale_{factor}\n\n    For details of nearest neighbor interpolation, please refer to Wikipedia: \n    https://en.wikipedia.org/wiki/Nearest-neighbor_interpolation.\n\n    For details of bilinear interpolation, please refer to Wikipedia: \n    https://en.wikipedia.org/wiki/Bilinear_interpolation.\n\n\n\n    Args:\n        input (Variable): The input tensor of image resize layer,\n                          This is a 4-D tensor of the shape\n                          (num_batches, channels, in_h, in_w).\n        out_shape(list|tuple|Variable|None): Output shape of image resize\n                                    layer, the shape is (out_h, out_w).\n                                    Default: None\n        scale(float|None): The multiplier for the input height or width. At\n             least one of :attr:`out_shape` or :attr:`scale` must be set. \n             And :attr:`out_shape` has a higher priority than :attr:`scale`. \n             Default: None.\n        name(str|None): A name for this layer(optional). If set None, the layer\n                        will be named automatically.\n        resample(str): The resample method. It supports \'BILINEAR\' and \'NEAREST\'\n                       currently.\n                       Default: \'BILINEAR\'\n        actual_shape(Variable): An optional input to specify output shape\n                                dynamically. If provided, image resize\n                                according to this given shape rather than\n                                :attr:`out_shape` and :attr:`scale` specifying\n                                shape. That is to say actual_shape has the\n                                highest priority. It is recommended to use\n                                actual_shape instead of :attr:`out_shape` if you\n                                want to specify output shape dynamically. When\n                                using actual_shape to specify output shape, one of\n                                :attr:`out_shape` and :attr:`scale` should also be\n                                set, otherwise errors would be occured in graph\n                                constructing stage.\n                                Default: None\n        align_corners(bool) :  An optional bool, If True, the centers of the 4 corner pixels of the \n                               input and output tensors are aligned, preserving the values at the \n                               corner pixels.\n                               Default: True\n        align_mode(int)  :  An optional for bilinear interpolation. can be \'0\' \n                            for src_idx = scale*(dst_indx+0.5)-0.5 , can be \'1\' for \n                            src_idx = scale*dst_index .\n\n    Returns:\n        Variable: The output is a 4-D tensor of the shape\n        (num_batches, channls, out_h, out_w).\n\n    Raises:\n        TypeError: out_shape should be a list or tuple or Variable.\n        TypeError: actual_shape should either be Variable or None.\n        ValueError: The \'resample\' of image_resize can only be \'BILINEAR\'\n                    or \'NEAREST\' currently.\n        ValueError: One of out_shape and scale must not be None.\n        ValueError: out_shape length should be 2.\n        ValueError: scale should be greater than zero.\n        TypeError: align_corners shoule be a bool value\n        ValueError: align_mode can only be \'0\' or \'1\'\n\n    Examples:\n        .. code-block:: python\n\n            input = fluid.layers.data(name="input", shape=[3,6,9], dtype="float32")\n            out = fluid.layers.image_resize(input, out_shape=[12, 12], resample="NEAREST")\n    '
    resample_methods = {
        'BILINEAR': 'bilinear',
        'NEAREST': 'nearest',
    }
    if (resample not in resample_methods):
        raise ValueError("The 'resample' of image_resize can only be 'BILINEAR' or 'NEAREST' currently.")
    resample_type = resample_methods[resample]
    if (not isinstance(align_corners, bool)):
        raise TypeError('Attr align_corners should be a bool value')
    if ((align_mode != 0) and (align_mode != 1)):
        raise ValueError('align_mode can only be 0 or 1')
    if ((out_shape is None) and (scale is None)):
        raise ValueError('One of out_shape and scale must not be None.')
    helper = LayerHelper('{}_interp'.format(resample_type), **locals())
    dtype = helper.input_dtype()

    def _is_list_or_turple_(data):
        return (isinstance(data, list) or isinstance(data, tuple))
    inputs = {
        'X': input,
    }
    attrs = {
        'out_h': 0,
        'out_w': 0,
        'interp_method': resample_type,
        'align_corners': align_corners,
        'align_mode': align_mode,
    }
    if (out_shape is not None):
        if isinstance(out_shape, Variable):
            warnings.warn('out_shape as Variable type is deprecated,                     it is recommended to use actual_shape instead of                     out_shape to specify output shape dynamically.')
            inputs['OutSize'] = out_shape
        else:
            if (not _is_list_or_turple_(out_shape)):
                raise TypeError('out_shape should be a list or tuple or Variable.')
            if (len(out_shape) != 2):
                raise ValueError('out_shape length should be 2.')
            out_shape = list(map(int, out_shape))
            attrs['out_h'] = out_shape[0]
            attrs['out_w'] = out_shape[1]
    else:
        if (scale <= 0):
            raise ValueError('scale should be greater than zero.')
        attrs['scale'] = float(scale)
    if isinstance(actual_shape, Variable):
        inputs['OutSize'] = actual_shape
    elif (actual_shape is not None):
        raise TypeError('actual_shape should either be Variable or None.')
    out = helper.create_variable_for_type_inference(dtype)
    helper.append_op(type='{}_interp'.format(resample_type), inputs=inputs, outputs={
        'Out': out,
    }, attrs=attrs)
    return out