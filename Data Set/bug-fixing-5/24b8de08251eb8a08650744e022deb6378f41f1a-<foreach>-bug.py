def foreach(body, data, init_states):
    'Run a for loop with user-defined computation over NDArrays on dimension 0.\n\n    This operator simulates a for loop and body has the computation for an iteration\n    of the for loop. It runs the computation in body on each slice from the input\n    NDArrays.\n\n    body takes two arguments as input and outputs a tuple of two elements,\n    as illustrated below:\n\n    out, states = body(data1, states)\n\n    data1 can be either an NDArray or a list of NDArrays. If data is an NDArray,\n    data1 is an NDArray. Otherwise, data1 is a list of NDArrays and has the same\n    size as data. states is a list of NDArrays and have the same size as init_states.\n    Similarly, out can be either an NDArray or a list of NDArrays, which are concatenated\n    as the first output of foreach; states from the last execution of body\n    are the second output of foreach.\n\n    The computation done by this operator is equivalent to the pseudo code below\n    when the input data is NDArray:\n\n    states = init_states\n    outs = []\n    for i in data.shape[0]:\n        s = data[i]\n        out, states = body(s, states)\n        outs.append(out)\n    outs = stack(*outs)\n\n\n    Parameters\n    ----------\n    body : a Python function.\n        Define computation in an iteration.\n    data: an NDArray or a list of NDArrays.\n        The input data.\n    init_states: an NDArray or nested lists of NDArrays.\n        The initial values of the loop states.\n    name: string.\n        The name of the operator.\n\n    Returns\n    -------\n    outputs: an NDArray or nested lists of NDArrays.\n        The output data concatenated from the output of all iterations.\n    states: an NDArray or nested lists of NDArrays.\n        The loop states in the last iteration.\n\n    Examples\n    --------\n    >>> step = lambda data, states: (data + states[0], [states[0] * 2])\n    >>> data = mx.nd.random.uniform(shape=(2, 10))\n    >>> states = [mx.nd.random.uniform(shape=(10))]\n    >>> outs, states = mx.nd.contrib.foreach(step, data, states)\n    '

    def check_input(inputs, in_type, msg):
        is_NDArray_or_list = True
        if isinstance(inputs, list):
            for i in inputs:
                if (not isinstance(i, in_type)):
                    is_NDArray_or_list = False
                    break
        else:
            is_NDArray_or_list = isinstance(inputs, in_type)
        assert is_NDArray_or_list, msg
    (flatten, _) = _flatten(data, 'foreach input')
    check_input(flatten, ndarray.NDArray, 'data should be an NDArray or a nested list of NDArrays')
    (flatten, _) = _flatten(init_states, 'foreach states')
    check_input(flatten, ndarray.NDArray, 'init_states should be an NDArray or a nested list of NDArrays')
    not_data_list = isinstance(data, ndarray.NDArray)
    num_iters = (data.shape[0] if not_data_list else data[0].shape[0])
    states = init_states
    outputs = []
    for i in range(num_iters):
        if not_data_list:
            eles = data[i]
        else:
            eles = [d[i] for d in data]
        (outs, states) = body(eles, states)
        (outs, out_fmt) = _flatten(outs, 'foreach output')
        outputs.append(outs)
    outputs = zip(*outputs)
    tmp_outputs = []
    for out in outputs:
        tmp_outputs.append(ndarray.op.stack(*out))
    outputs = tmp_outputs
    (outputs, _) = _regroup(outputs, out_fmt)
    return (outputs, states)