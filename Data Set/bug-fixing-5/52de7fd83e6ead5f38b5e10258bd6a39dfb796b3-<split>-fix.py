def split(input, num_or_sections, dim=(- 1), name=None):
    "\n    Split the input tensor into multiple sub-tensors.\n\n    Args:\n        input (Variable): The input variable which is a Tensor or LoDTensor.\n        num_or_sections (int|list): If :attr:`num_or_sections` is an integer,\n            then the integer indicates the number of equal sized sub-tensors\n            that the tensor will be divided into. If :attr:`num_or_sections`\n            is a list of integers, the length of list indicates the number of\n            sub-tensors and the integers indicate the sizes of sub-tensors'\n            :attr:`dim` dimension orderly.\n        dim (int): The dimension along which to split. If :math:`dim < 0`, the\n            dimension to split along is :math:`rank(input) + dim`.\n        name(str|None): A name for this layer(optional). If set None, the layer\n                       will be named automatically.\n\n    Returns:\n        list(Variable): The list of segmented tensor variables.\n\n    Examples:\n        .. code-block:: python\n\n            # x is a Tensor variable with shape [3, 9, 5]:\n            x0, x1, x2 = fluid.layers.split(x, num_or_sections=3, dim=1)\n            x0.shape  # [3, 3, 5]\n            x1.shape  # [3, 3, 5]\n            x2.shape  # [3, 3, 5]\n            x0, x1, x2 = fluid.layers.split(\n                x, num_or_sections=[2, 3, 4], dim=1)\n            x0.shape  # [3, 2, 5]\n            x1.shape  # [3, 3, 5]\n            x2.shape  # [3, 4, 5]\n    "
    helper = LayerHelper('split', **locals())
    input_shape = input.shape
    dim = ((len(input_shape) + dim) if (dim < 0) else dim)
    if isinstance(num_or_sections, int):
        assert (num_or_sections > 1), 'num_or_sections must be more than 1.'
        num = num_or_sections
    else:
        assert (len(num_or_sections) <= input_shape[dim]), 'len(num_or_sections) must not be more than input.shape[dim].'
        num = len(num_or_sections)
    outs = [helper.create_variable_for_type_inference(dtype=helper.input_dtype()) for i in range(num)]
    helper.append_op(type='split', inputs={
        'X': input,
    }, outputs={
        'Out': outs,
    }, attrs={
        'num': (num_or_sections if isinstance(num_or_sections, int) else 0),
        'sections': (num_or_sections if isinstance(num_or_sections, list) else []),
        'axis': dim,
    })
    return outs