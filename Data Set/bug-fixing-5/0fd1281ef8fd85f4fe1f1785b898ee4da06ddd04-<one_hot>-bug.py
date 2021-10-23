def one_hot(input, depth, allow_out_of_range=False):
    '\n\n    **WARING:** This OP requires the last dimension of Tensor shape must be equal to 1.\n    This OP will be deprecated in a future release. It is recommended to use fluid. :ref:`api_fluid_one_hot` .\n\n    The operator converts each id in the input to an one-hot vector with a\n    :attr:`depth` length. The value in the vector dimension corresponding to the id\n    is 1, and the value in the remaining dimension is 0.\n\n    The shape of output Tensor or LoDTensor is generated by adding :attr:`depth` dimension\n    behind the last dimension of the input shape.\n\n    .. code-block:: text\n\n        Example 1 (allow_out_of_range=False):\n\n        input:\n            X.shape = [4, 1]\n            X.data = [[1], [1], [3], [0]]\n            depth = 4\n\n        output:\n            Out.shape = [4, 4]\n            Out.data = [[0., 1., 0., 0.],\n                        [0., 1., 0., 0.],\n                        [0., 0., 0., 1.],\n                        [1., 0., 0., 0.]]\n\n        Example 2 (allow_out_of_range=True):\n\n        input:\n            X.shape = [4, 1]\n            X.data = [[1], [1], [5], [0]]\n            depth = 4\n            allow_out_of_range = True\n\n        output:\n            Out.shape = [4, 4]\n            Out.data = [[0., 1., 0., 0.],\n                        [0., 1., 0., 0.], \n                        [0., 0., 0., 0.], # This id is 5, which goes beyond depth, so set it all-zeros data.\n                        [1., 0., 0., 0.]]\n\n        Example 3 (allow_out_of_range=False):\n\n        input:\n            X.shape = [4, 1]\n            X.data = [[1], [1], [5], [0]]\n            depth = 4\n            allow_out_of_range = False\n\n        output: Throw an exception for Illegal value\n            The second dimension in X is 5, which is greater than depth.  \n            Allow_out_of_range =False means that does not allow the word id to exceed depth,\n            so it throws an exception.\n\n    Args:\n        input(Variable): Tensor or LoDTensor with shape :math:`[N_1, N_2, ..., N_k, 1]` ,\n            which contains at least one dimension and the last dimension must be 1.\n            The data type is int32 or int64.\n        depth(scalar): An integer defining the :attr:`depth` of the one hot dimension. If input \n            is word id, depth is generally the dictionary size.\n        allow_out_of_range(bool): A bool value indicating whether the input\n            indices could be out of range :math:`[0, depth)` . When input indices are\n            out of range, exceptions :code:`Illegal value` is raised if :attr:`allow_out_of_range`\n            is False, or zero-filling representations is created if it is set True.\n            Default: False.\n\n    Returns:\n        Variable: The one-hot representations of input. A Tensor or LoDTensor with type float32.\n\n    Examples:\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n            # Correspond to the first example above, where label.shape is [4, 1] and one_hot_label.shape is [4, 4].\n            label = fluid.data(name="label", shape=[4, 1], dtype="int64")\n            one_hot_label = fluid.layers.one_hot(input=label, depth=4)\n    '
    helper = LayerHelper('one_hot', **locals())
    one_hot_out = helper.create_variable_for_type_inference(dtype='float32')
    if in_dygraph_mode():
        inputs = {
            'X': input,
        }
        attrs = {
            'depth': depth,
        }
    elif (not isinstance(depth, Variable)):
        inputs = {
            'X': input,
        }
        attrs = {
            'depth': depth,
        }
    else:
        depth.stop_gradient = True
        inputs = {
            'X': input,
            'depth_tensor': depth,
        }
        attrs = {
            
        }
    helper.append_op(type='one_hot', inputs=inputs, attrs=attrs, outputs={
        'Out': one_hot_out,
    })
    one_hot_out.stop_gradient = True
    return one_hot_out