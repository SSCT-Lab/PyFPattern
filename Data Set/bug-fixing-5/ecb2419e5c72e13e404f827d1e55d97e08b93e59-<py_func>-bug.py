@templatedoc()
def py_func(func, x, out, backward_func=None, skip_vars_in_backward_input=None):
    "\n    This API is used to register customized OP to Fluid. The forward  function \n    of the registered OP is ``func`` and the backward function of that is \n    ``backward_func``. Paddle will call ``func`` at forward runtime  and call \n    ``backward_func`` at backward runtime(if ``backward_func`` is not  None). \n    ``x`` is the input of ``func``, whose type must be LoDTensor; ``out`` is \n    the output of ``func``, whose type can be either LoDTensor or NumPy array.\n\n    The input of the backward function ``backward_func`` is ``x``, ``out`` and \n    the gradient of ``out``. If some variables of ``out`` have no gradient, the \n    relevant input variable of ``backward_func`` is None. If some variables of \n    ``x`` do not have a gradient, the user should return None in ``backward_func``.\n\n    The data type and shape of ``out`` should also be set correctly before this \n    API is called, and the data type and shape of the gradient of ``out`` and \n    ``x`` will be inferred automatically.\n\n    This API can also be used to debug the neural network by setting the ``func``\n    as a function that only print variables.\n\n    Args:\n        func (callable): The forward function of the registered OP. When the network\n            is running, the forward output ``out`` will be calculated according to this \n            function and the forward input ``x``.\n        x (Variable): The input of the forward function ``func``, its type can be \n            Variable | tuple[Variable] | list[Variale], in which Variable is LoDTensor.\n        out (Variable): The output of the forward function ``func``, its type can be\n            Variable | tuple[Variable] | list[Variale], in which Variable can be either \n            LoDTensor or NumPy array. Since Paddle cannot automatically infer the shape\n            and data type of ``out``, ``out`` must be created in advance.\n        backward_func (callable, optional): The backward function of the registered OP. \n            Its default value is None, which means there is no reverse calculation. If \n            it is not None, ``backward_func`` is called to calculate the gradient of \n            ``x`` when the network is at backward runtime.\n        skip_vars_in_backward_input (Variable, optional): It's used to limit the input \n            variable list of ``backward_func``, and it can be single Variable, tuple[Variable]\n            or list[Variable]. It must belong to either ``x`` or ``out``. The default \n            value is None, which means that no variables need to be removed from ``x`` \n            and ``out``. If it is not None, these variables will not be the input of \n            ``backward_func``. This parameter is only useful when ``backward_func`` is \n            not None.\n    \n    Returns: \n        Variable: The output ``out`` of the forward function ``func``.\n\n    Examples:\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n            import six\n\n            def create_tmp_var(name, dtype, shape):\n            return fluid.default_main_program().current_block().create_var(\n            name=name, dtype=dtype, shape=shape)\n\n            # Tanh activation function provided by Paddle C++ op\n            # Here, tanh is used as an example to show how to use py_func\n            def tanh(x):\n                return np.tanh(x)\n\n            # Skip forward input x\n            def tanh_grad(y, dy):\n                return np.array(dy) * (1 - np.square(np.array(y)))\n\n            def debug_func(x):\n                print(x)\n\n            def simple_net(img, label):\n                hidden = img\n                for idx in six.moves.range(4):\n                    hidden = fluid.layers.fc(hidden, size=200)\n                    new_hidden = create_tmp_var(name='hidden_{}'.format(idx),\n                        dtype=hidden.dtype, shape=hidden.shape)\n\n                    # User-defined forward and backward \n                    hidden = fluid.layers.py_func(func=tanh, x=hidden,\n                        out=new_hidden, backward_func=tanh_grad,\n                        skip_vars_in_backward_input=hidden)\n\n                    # User-defined debugging layer, which can print out variable details\n                    fluid.layers.py_func(func=debug_func, x=hidden, out=None)\n\n                prediction = fluid.layers.fc(hidden, size=10, act='softmax')\n                loss = fluid.layers.cross_entropy(input=prediction, label=label)\n                return fluid.layers.mean(loss)\n    "
    helper = LayerHelper('py_func', **locals())
    if (x is None):
        x = []
    elif isinstance(x, Variable):
        x = [x]
    elif isinstance(x, tuple):
        x = list(x)
    elif (not isinstance(x, (list, tuple, Variable))):
        raise TypeError('Input must be Variable/list(Variable)/tuple(Variable)')
    if (out is None):
        out_list = []
    elif isinstance(out, Variable):
        out_list = [out]
    elif isinstance(out, tuple):
        out_list = list(out)
    elif (not isinstance(x, (list, tuple, Variable))):
        raise TypeError('Output must be Variable/list(Variable)/tuple(Variable)')
    fwd_func_id = PyFuncRegistry(func).id
    bwd_func_id = (PyFuncRegistry(backward_func).id if (backward_func is not None) else (- 1))
    for each_out in out_list:
        if (len(each_out.shape) == 0):
            raise ValueError('Output shapes of py_func op should be provided by users manually')
    backward_skip_vars = set()
    if ((backward_func is not None) and (skip_vars_in_backward_input is not None)):
        if isinstance(skip_vars_in_backward_input, Variable):
            skip_vars_in_backward_input = [skip_vars_in_backward_input]
        fwd_in_out = [v.name for v in x]
        fwd_in_out.extend([v.name for v in out_list])
        fwd_in_out = set(fwd_in_out)
        backward_skip_vars = set()
        for v in skip_vars_in_backward_input:
            if (not (v.name in fwd_in_out)):
                raise ValueError('Variable {} is not found in forward inputs and outputs'.format(v.name))
            backward_skip_vars.add(v.name)
    helper.append_op(type='py_func', inputs={
        'X': x,
    }, outputs={
        'Out': out_list,
    }, attrs={
        'forward_callable_id': fwd_func_id,
        'backward_callable_id': bwd_func_id,
        'backward_skip_vars': list(backward_skip_vars),
    })
    return out