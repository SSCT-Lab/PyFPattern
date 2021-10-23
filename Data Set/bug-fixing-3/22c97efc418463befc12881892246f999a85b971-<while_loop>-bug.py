def while_loop(cond, func, loop_vars, max_iterations=None, name='while_loop'):
    "Run a while loop with user-defined computation and loop condition.\n\n    This operator simulates a while loop which iterately does customized computation\n    as long as the condition is satisfied.\n\n    `loop_vars` is a list of Symbols on which the computation uses.\n\n    `cond` is a user-defined function, used as the loop condition.\n    It consumes `loop_vars`, and produces a scalar MXNet symbol,\n    indicating the termination of the loop.\n    The loop ends when `cond` returns false (zero).\n    The `cond` is variadic, and its signature should be\n    `cond(*loop_vars) => Symbol`.\n\n    `func` is a user-defined function, used as the loop body.\n    It also consumes `loop_vars`, and produces `step_output` and `new_loop_vars` at each step.\n    In each step, `step_output` should contain the same number elements.\n    Through all steps, the i-th element of `step_output` should have the same shape and dtype.\n    Also, `new_loop_vars` should contain the same number of elements as `loop_vars`,\n    and the corresponding element should have the same shape and dtype.\n    The `func` is variadic, and its signature should be\n    `func(*loop_vars) => (List[Symbol] step_output, List[Symbol] new_loop_vars)`.\n\n    `max_iterations` is a scalar that defines the maximum number of iterations allowed.\n\n    This function returns two lists.\n    The first list has the length of `|step_output|`,\n    in which the i-th element are all i-th elements of\n    `step_output` from all steps, stacked along axis 0.\n    The second list has the length of `|loop_vars|`,\n    which represents final states of loop variables.\n\n    .. warning::\n\n       For now, the axis 0 of all Symbols in the first list are `max_iterations`,\n       due to lack of dynamic shape inference.\n\n    .. warning::\n\n       Even if `cond` is never satisfied,\n       while_loop returns a list of outputs with inferred dtype and shape.\n       This is different from the Symbol version,\n       where in this case `step_outputs` are assumed as an empty list.\n\n    Parameters\n    ----------\n    cond: a Python function.\n        The loop condition.\n    func: a Python function.\n        The loop body.\n    loop_vars: list of Symbol.\n        The initial values of the loop variables.\n    max_iterations: a python int.\n        Maximum number of iterations.\n\n    Returns\n    ------\n    outputs: list of Symbols\n        stacked output from each step\n    states: list of Symbols\n        final state\n\n    Examples\n    --------\n    >>> cond = lambda i, s: i <= 5\n    >>> func = lambda i, s: ([i + s], [i + 1, s + i])\n    >>> loop_vars = (mx.sym.var('i'), mx.sym.var('s'))\n    >>> outputs, states = mx.sym.contrib.while_loop(cond, func, loop_vars, max_iterations=10)\n    "

    def _to_python_scalar(inputs, type_, name):
        'Converts "inputs", possibly typed mxnet NDArray, a numpy ndarray, other python types,\n        to the given type\n        '
        if hasattr(inputs, 'asscalar'):
            inputs = inputs.asscalar()
        try:
            inputs = type_(inputs)
        except:
            raise ValueError(('Cannot convert %s to python %s' % (name, type_.__name__)))
        return inputs

    def _to_symbol_tuple(inputs, name):
        'Converts "inputs", possibly a single mxnet Symbol, a list of mxnet Symbol,\n        a tuple of mxnet Symbol, into a tuple of Symbol\n        '
        if isinstance(inputs, list):
            inputs = tuple(inputs)
        if isinstance(inputs, Symbol):
            inputs = (inputs,)
        if (not isinstance(inputs, tuple)):
            raise ValueError(('%s must be a Symbol, or a tuple or list of Symbol' % (name,)))
        for item in inputs:
            if (not isinstance(item, Symbol)):
                raise ValueError(('%s must be a Symbol, or a tuple or list of Symbol' % (name,)))
        return inputs

    def _cond_wrapper(loop_vars):
        result = cond(*loop_vars)
        if (not isinstance(result, Symbol)):
            raise ValueError('Return of cond must be a Symbol')
        return ([], [result])

    def _func_wrapper(loop_vars):
        'This wrapper unifies\n             "func: loop_vars -> new_loop_vars"\n         and "func: loop_vars -> (step_output, new_loop_vars)"\n        into "func: loop_vars -> (list of step_outputs, tuple of new_loop_vars)\n        '
        (step_output, new_loop_vars) = func(*loop_vars)
        if (step_output is None):
            step_output = []
        if (new_loop_vars is None):
            new_loop_vars = []
        step_output = _to_symbol_tuple(step_output, 'step_output')
        new_loop_vars = _to_symbol_tuple(new_loop_vars, 'new_loop_vars')
        if (len(loop_vars) != len(new_loop_vars)):
            raise ValueError('The number of loop_vars should be consistent during the loop')
        return (list(step_output), list(new_loop_vars))

    def _create_subgraph(graph_vars, graph_func, subgraph_name):
        with AttrScope(__subgraph_name__=subgraph_name):
            new_graph_vars = [symbol.var(sym.name) for sym in graph_vars]
            (outputs, final_state) = graph_func(new_graph_vars)
            num_out_data = len(outputs)
            num_outputs = (len(outputs) + len(final_state))
            all_input_names = symbol.Group((outputs + final_state)).list_inputs()
            make_identity = (lambda x: (symbol.op.identity(x) if (x.name in all_input_names) else x))
            graph = symbol.Group(list(map(make_identity, (outputs + final_state))))
        return (graph, num_out_data, num_outputs)

    def _union_inputs(*graphs):
        inputs = []
        locs = []
        input_id_to_loc = {
            
        }
        for graph in graphs:
            name_to_input_syms = {sym.name: sym for sym in _get_graph_inputs(graph)}
            name_to_loop_vars = {sym.name: sym for sym in loop_vars}
            name_to_cut_g_syms = {sym.list_outputs()[0]: sym for sym in _cut_subgraph(graph)}
            name_to_var_locs = {sym.name: i for (i, sym) in enumerate(loop_vars)}
            input_locs = []
            var_locs = ([(- 1)] * len(loop_vars))
            for name in graph.list_inputs():
                assert (name in name_to_input_syms)
                if (name in name_to_loop_vars):
                    sym = name_to_loop_vars[name]
                elif (name in name_to_cut_g_syms):
                    sym = name_to_cut_g_syms[name]
                else:
                    sym = copy.deepcopy(name_to_input_syms[name])
                if (id(sym) in input_id_to_loc):
                    loc = input_id_to_loc[id(sym)]
                else:
                    loc = len(input_id_to_loc)
                    inputs.append(sym)
                    input_id_to_loc[id(sym)] = loc
                input_locs.append(loc)
                if (name in name_to_var_locs):
                    var_locs[name_to_var_locs[name]] = (len(input_locs) - 1)
            locs.append((input_locs, var_locs))
        return (inputs, locs)
    if (max_iterations is None):
        raise ValueError('max_iterations should be specified')
    max_iterations = _to_python_scalar(max_iterations, int, 'max_iteration')
    loop_vars = _to_symbol_tuple(loop_vars, 'loop_vars')
    if (len(loop_vars) == 0):
        raise ValueError('loop_vars should contain at least one element')
    (cond_g, num_out_data, num_outputs) = _create_subgraph(loop_vars, _cond_wrapper, (name + '_cond'))
    assert (num_out_data == 0)
    assert (num_outputs == 1)
    (func_g, num_out_data, num_outputs) = _create_subgraph(loop_vars, _func_wrapper, (name + '_func'))
    (input_syms, ((cond_input_locs, _), (func_input_locs, func_var_locs))) = _union_inputs(cond_g, func_g)
    for (i_th, loc) in enumerate(func_var_locs, 1):
        if (loc == (- 1)):
            raise ValueError(("The %d-th loop_var doesn't involve into the computation" % i_th))
    result = symbol._internal._while_loop(cond_g, func_g, *input_syms, max_iterations=max_iterations, cond_input_locs=cond_input_locs, func_input_locs=func_input_locs, func_var_locs=func_var_locs, num_out_data=num_out_data, num_outputs=num_outputs)
    outputs = [result[i] for i in range(num_out_data)]
    final_loop_vars = [result[i] for i in range(num_out_data, num_outputs)]
    return (outputs, final_loop_vars)