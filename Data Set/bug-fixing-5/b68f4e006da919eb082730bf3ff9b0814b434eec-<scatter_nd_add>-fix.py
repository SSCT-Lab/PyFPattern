def scatter_nd_add(ref, index, updates, name=None):
    "\n    **Scatter_nd_add Layer**\n\n    Output is obtained by applying sparse addition to a single value\n    or slice in a Variable. \n\n    :attr:`ref` is a Tensor with rank :math:`R` \n    and :attr:`index` is a Tensor with rank :math:`K` . Thus, :attr:`index` \n    has shape :math:`[i_0, i_1, ..., i_{K-2}, Q]` where :math:`Q \\leq R` . :attr:`updates` \n    is a Tensor with rank :math:`K - 1 + R - Q` and its\n    shape is :math:`index.shape[:-1] + ref.shape[index.shape[-1]:]` .\n\n    According to the :math:`[i_0, i_1, ..., i_{K-2}]` of :attr:`index` ,\n    add the corresponding :attr:`updates` slice to the :attr:`ref` slice\n    which is obtained by the last one dimension of :attr:`index` .\n\n    .. code-block:: text\n        \n        Given:\n\n        * Case 1:\n            ref = [0, 1, 2, 3, 4, 5]\n            index = [[1], [2], [3], [1]]\n            updates = [9, 10, 11, 12]\n\n          we get:\n             \n            output = [0, 22, 12, 14, 4, 5]\n\n        * Case 2:\n            ref = [[65, 17], [-14, -25]]\n            index = [[], []]\n            updates = [[[-1, -2], [1, 2]],\n                       [[3, 4], [-3, -4]]]\n            ref.shape = (2, 2)\n            index.shape = (2, 0)\n            updates.shape = (2, 2, 2)\n\n          we get:\n             \n            output = [[67, 19], [-16, -27]]\n\n    Args:\n        ref (Variable): The ref input. Its dtype should be float32, float64.\n        index (Variable): The index input with rank > 1 and index.shape[-1] <= ref.rank.\n                          Its dtype should be int32 or int64 as it is used as indexes.\n        updates (Variable): The updated value of scatter_nd_add op, and it must have the same dtype\n                            as ref. It must have the shape index.shape[:-1] + ref.shape[index.shape[-1]:].\n        name (str|None): The output variable name. If set None, the layer will be named automatically.\n\n    Returns:\n        output (Variable): The output is a tensor with the same shape and dtype as ref.\n\n    Examples:\n\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n\n            ref = fluid.data(name='ref', shape=[3, 5, 9, 10], dtype='float32')\n            index = fluid.data(name='index', shape=[3, 2], dtype='int32')\n            updates = fluid.data(name='update', shape=[3, 9, 10], dtype='float32')\n\n            output = fluid.layers.scatter_nd_add(ref, index, updates)\n    "
    if (ref.dtype != updates.dtype):
        raise ValueError('ref and updates must have same data type.')
    helper = LayerHelper('scatter_nd_add', **locals())
    dtype = helper.input_dtype(input_param_name='ref')
    if (name is None):
        output = helper.create_variable_for_type_inference(dtype)
    else:
        output = helper.create_variable(name=name, dtype=dtype, persistable=False)
    helper.append_op(type='scatter_nd_add', inputs={
        'X': ref,
        'Index': index,
        'Updates': updates,
    }, outputs={
        'Out': output,
    })
    return output