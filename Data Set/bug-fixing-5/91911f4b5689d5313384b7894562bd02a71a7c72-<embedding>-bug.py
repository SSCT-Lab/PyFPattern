def embedding(input, size, is_sparse=False, param_attr=None, dtype='float32'):
    "\n    **Embedding Layer**\n\n    This layer is used to lookup a vector of IDs, provided by *input*, in a lookup table.\n    The result of this lookup is the embedding of each ID in the *input*.\n\n    All the input variables are passed in as local variables to the LayerHelper\n    constructor.\n\n    Args:\n       input(Variable): Input to the function\n       size(int): Output size\n       is_sparse(bool): Boolean flag that specifying whether the input is sparse\n       param_attr(ParamAttr): Parameters for this layer\n       dtype(np.dtype|core.DataType|str): The type of data : float32, float_16, int etc\n\n    Returns:\n        Variable: The tensor variable storing the embeddings of the                   supplied inputs.\n\n    Examples:\n        .. code-block:: python\n\n          data = fluid.layers.data(name='ids', shape=[32, 32], dtype='float32')\n          fc = fluid.layers.embedding(input=data, size=16)\n    "
    helper = LayerHelper('embedding', **locals())
    w = helper.create_parameter(attr=helper.param_attr, shape=size, dtype=dtype, is_bias=False)
    tmp = helper.create_tmp_variable(dtype)
    helper.append_op(type='lookup_table', inputs={
        'Ids': input,
        'W': w,
    }, outputs={
        'Out': tmp,
    }, attrs={
        'is_sparse': is_sparse,
    })
    return tmp