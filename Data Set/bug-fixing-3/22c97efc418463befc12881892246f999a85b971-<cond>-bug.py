def cond(pred, then_func, else_func, name='cond'):
    "Run an if-then-else using user-defined condition and computation\n\n    This operator simulates a if-like branch which chooses to do one of\n    the two customized computations according to the specified condition.\n\n    `pred` is a scalar MXNet Symbol,\n    indicating which branch of computation should be used.\n\n    `then_func` is a user-defined function, used as computation of the then branch.\n    It produces `outputs`, which is a list of Symbols.\n    The signature of `then_func` should be\n    `then_func() => List[Symbol]`.\n\n    `else_func` is a user-defined function, used as computation of the else branch.\n    It produces `outputs`, which is a list of Symbols.\n    The signature of `else_func` should be\n    `else_func() => List[Symbol]`.\n\n    The `outputs` produces by `then_func` and `else_func` should have the same number\n    of elements, all of which should be in the same shape, of the same dtype and stype.\n\n    This function returns a list of symbols, representing the computation result.\n\n    Parameters\n    ----------\n    pred: a MXNet Symbol representing a scalar.\n        The branch condition.\n    then_func: a Python function.\n        The computation to be executed if `pred` is true.\n    else_func: a Python function.\n        The computation to be executed if `pred` is false.\n\n    Returns\n    -------\n    outputs: a list of Symbols, representing the result of computation.\n\n    Examples\n    --------\n    >>> a, b = mx.sym.var('a'), mx.sym.var('b')\n    >>> pred = a * b < 5\n    >>> then_func = lambda: (a + 5) * (b + 5)\n    >>> else_func = lambda: (a - 5) * (b - 5)\n    >>> outputs = mx.sym.contrib.cond(pred, then_func, else_func)\n    "

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

    def _create_subgraph(graph_vars, graph_func, subgraph_name):
        with AttrScope(__subgraph_name__=subgraph_name):
            new_graph_vars = [symbol.var(sym.name) for sym in graph_vars]
            outputs = graph_func(*new_graph_vars)
            outputs = _to_symbol_tuple(outputs, 'outputs')
            num_outputs = len(outputs)
            all_input_names = symbol.Group(outputs).list_inputs()
            make_identity = (lambda x: (symbol.op.identity(x) if (x.name in all_input_names) else x))
            graph = symbol.Group(list(map(make_identity, outputs)))
        return (graph, num_outputs)

    def _union_inputs(*graphs):
        inputs = []
        locs = []
        input_id_to_loc = {
            
        }
        for graph in graphs:
            name_to_input_syms = {sym.name: sym for sym in _get_graph_inputs(graph)}
            name_to_input_vars = {sym.name: sym for sym in inputs}
            name_to_cut_g_syms = {sym.list_outputs()[0]: sym for sym in _cut_subgraph(graph)}
            input_locs = []
            for name in graph.list_inputs():
                assert (name in name_to_input_syms)
                if (name in name_to_input_vars):
                    sym = name_to_input_vars[name]
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
            locs.append(input_locs)
        return (inputs, locs)
    inputs = []
    (cond_g, cond_num_outputs) = _create_subgraph(inputs, (lambda : pred), (name + '_pred'))
    if (cond_num_outputs != 1):
        raise ValueError('pred should always be a single output')
    (then_g, then_num_outputs) = _create_subgraph(inputs, then_func, (name + '_then'))
    (else_g, else_num_outputs) = _create_subgraph(inputs, else_func, (name + '_else'))
    if (then_num_outputs != else_num_outputs):
        raise ValueError('Number of outputs differs between then-branch and else-branch')
    (input_syms, (cond_input_locs, then_input_locs, else_input_locs)) = _union_inputs(cond_g, then_g, else_g)
    result = symbol._internal._cond(cond_g, then_g, else_g, *input_syms, cond_input_locs=cond_input_locs, then_input_locs=then_input_locs, else_input_locs=else_input_locs, num_outputs=then_num_outputs)
    result = _to_symbol_tuple(result, 'result')
    return list(result)