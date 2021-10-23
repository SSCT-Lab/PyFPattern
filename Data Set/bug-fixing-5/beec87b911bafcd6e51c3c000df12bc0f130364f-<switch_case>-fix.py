def switch_case(branch_index, branch_fns, default=None, name=None):
    "\n    This operator is like a C++ switch/case statement.\n\n    Args:\n        branch_index(Variable): A Tensor with shape [1] to specify which branch to execute. The data type is ``int32``, ``int64`` or ``uint8``.\n        branch_fns(dict|list|tuple): If it's a list or tuple, the elements in it could be pairs of (int, callable) or simple callables whose actual index will be used as the index of callable. If it's a dict, its key is a python integer and the value is a callable. All callables return the same structure of Tensors.\n        default(callable, optional): Callable that returns a structure of Tensors.\n        name(str, optional): The default value is None. Normally there is no need for user to set this property. For more information, please refer to :ref:`api_guide_Name`.\n\n    Returns:\n        Variable|list(Variable): Tensors returned by the callable specified by ``branch_index`` in ``branch_fns``,\n        or Tensors returned by ``default`` if ``default`` is not None and no index matches in ``branch_fns``,\n        or Tensors returned by the callable with the max index in ``branch_fns`` if ``default`` is None and no index matches in ``branch_fns``.\n\n    Raises:\n        TypeError: If the type of ``branch_index`` is not Variable.\n        TypeError: If the data type of ``branch_index`` is not ``int32``, ``int64`` or ``uint8``.\n        TypeError: If the type of ``branch_fns`` is not dict, list or tuple.\n        TypeError: If the elements of ``branch_fns`` is not 2-tuple.\n        TypeError: If the first element of 2-tuple in ``branch_fns`` is not integer.\n        ValueError: If the first element of 2-tuple in ``branch_fns`` is not unique.\n        TypeError: If the second element of 2-tuple in ``branch_fns`` is not callable.\n        TypeError: If ``default`` is not None but it is not callable.\n\n    Examples:\n        .. code-block:: python\n\n            import paddle.fluid as fluid\n            import paddle.fluid.layers as layers\n\n            def fn_1():\n                return layers.fill_constant(shape=[1, 2], dtype='float32', value=1)\n\n            def fn_2():\n                return layers.fill_constant(shape=[2, 2], dtype='int32', value=2)\n\n            def fn_3():\n                return layers.fill_constant(shape=[3], dtype='int32', value=3)\n\n            main_program = fluid.default_startup_program()\n            startup_program = fluid.default_main_program()\n            with fluid.program_guard(main_program, startup_program):\n                index_1 = layers.fill_constant(shape=[1], dtype='int32', value=1)\n                index_2 = layers.fill_constant(shape=[1], dtype='int32', value=2)\n\n                out_1 = layers.switch_case(\n                    branch_index=index_1,\n                    branch_fns={1: fn_1, 2: fn_2},\n                    default=fn_3)\n\n                out_2 = layers.switch_case(\n                    branch_index=index_2,\n                    branch_fns=[(1, fn_1), (2, fn_2)],\n                    default=fn_3)\n\n                # Argument default is None and no index matches. fn_3 will be called because of the max index 7.\n                out_3 = layers.switch_case(\n                    branch_index=index_2,\n                    branch_fns=[(0, fn_1), (4, fn_2), (7, fn_3)])\n\n                exe = fluid.Executor(fluid.CPUPlace())\n                res_1, res_2, res_3 = exe.run(main_program,\n                                              fetch_list=[out_1, out_2, out_3])\n                print(res_1)  # [[1. 1.]]\n                print(res_2)  # [[2 2] [2 2]]\n                print(res_3)  # [3 3 3]\n    "
    helper = LayerHelper('switch_case', **locals())

    def _check_args(branch_index, branch_fns, default):
        if (not isinstance(branch_index, Variable)):
            raise TypeError(_error_message('The type', 'branch_index', 'switch_case', 'Variable', type(branch_index)))
        if (convert_dtype(branch_index.dtype) not in ['uint8', 'int32', 'int64']):
            raise TypeError(_error_message('The data type', 'branch_index', 'switch_case', 'uint8, int32 or int64', convert_dtype(branch_index.dtype)))
        if (convert_dtype(branch_index.dtype) != 'int64'):
            branch_index = cast(branch_index, 'int64')
        if (not isinstance(branch_fns, (list, tuple, dict))):
            raise TypeError(_error_message('The type', 'branch_fns', 'switch_case', 'dict, tuple or list', type(branch_fns)))
        branch_fns = (branch_fns.items() if isinstance(branch_fns, dict) else branch_fns)
        branch_fns = (list(enumerate(branch_fns)) if all((callable(fn) for fn in branch_fns)) else branch_fns)
        keys_of_fns = []
        for index_fn_pair in branch_fns:
            if (not isinstance(index_fn_pair, tuple)):
                raise TypeError(_error_message("The elements' type", 'branch_fns', 'switch_case', 'tuple', type(branch_fns)))
            if (len(index_fn_pair) != 2):
                raise TypeError(_error_message("The tuple's size", 'branch_fns', 'switch_case', '2', (str(len(index_fn_pair)) + '-tuple')))
            (key, fn) = index_fn_pair
            if (not isinstance(key, int)):
                raise TypeError(_error_message("The key's type", 'branch_fns', 'switch_case', 'int', type(key)))
            if (key in keys_of_fns):
                raise ValueError("The key in 'branch_fns' must be unique, but '{}' appears more than once.".format(key))
            else:
                keys_of_fns.append(key)
            if (not callable(fn)):
                raise TypeError(_error_message('The type of function for key {}'.format(key), 'branch_fns', 'switch_case', 'callable', type(fn)))
        if (default is None):
            default = sorted(branch_fns)[(- 1)][1]
            branch_fns = sorted(branch_fns)[:(- 1)]
        elif (not callable(default)):
            raise TypeError('The default in Op(case) must be callable.')
        pred_fn_pairs = []
        for (index, fn) in branch_fns:
            new_index = fill_constant(shape=[1], dtype='int64', value=index)
            pred = equal(branch_index, new_index)
            pred_fn_pairs.append((pred, fn))
        return (pred_fn_pairs, default)
    (pred_fn_pairs, default) = _check_args(branch_index, branch_fns, default)
    false_fn = default
    for (pred, true_fn) in pred_fn_pairs:
        false_fn = partial(cond, pred=pred, true_fn=true_fn, false_fn=false_fn)
    final_fn = false_fn
    return final_fn()