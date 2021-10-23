def build_computational_graph(outputs, remove_split=True, variable_style=_var_style, function_style=_func_style, rankdir='TB', remove_variable=False, show_name=True):
    "Builds a graph of functions and variables backward-reachable from outputs.\n\n    Args:\n        outputs(list): nodes from which the graph is constructed.\n            Each element of outputs must be either :class:`~chainer.Variable`\n            object, :class:`~chainer.variable.VariableNode` object, or\n            :class:`~chainer.FunctionNode` object.\n        remove_split(bool): It must be ``True``. This argument is left for\n            backward compatibility.\n        variable_style(dict): Dot node style for variable.\n            Possible keys are 'shape', 'color', 'fillcolor', 'style', and etc.\n        function_style(dict): Dot node style for function.\n        rankdir (str): Direction of the graph that must be\n            TB (top to bottom), BT (bottom to top), LR (left to right)\n            or RL (right to left).\n        remove_variable (bool): If ``True``, :class:`VariableNode`\\ s are\n            removed from the resulting computational graph. Only\n            :class:`FunctionNode`\\ s are shown in the output.\n        show_name (bool): If ``True``, the ``name`` attribute of each node is\n            added to the label of the node. Default is ``True``.\n\n    Returns:\n        ComputationalGraph: A graph consisting of nodes and edges that\n        are backward-reachable from at least one of ``outputs``.\n\n        If ``unchain_backward`` was called in some variable in the\n        computational graph before this function, backward step is\n        stopped at this variable.\n\n        For example, suppose that computational graph is as follows::\n\n                |--> f ---> y\n            x --+\n                |--> g ---> z\n\n        Let ``outputs = [y, z]``.\n        Then the full graph is emitted.\n\n        Next, let ``outputs = [y]``. Note that ``z`` and ``g``\n        are not backward-reachable from ``y``.\n        The resulting graph would be following::\n\n            x ---> f ---> y\n\n        See :class:`TestGraphBuilder` for details.\n\n    .. note::\n\n        The default behavior of :class:`~chainer.ComputationalGraph` has been\n        changed from v1.23.0, so that it ouputs the richest representation of\n        a graph as default, namely, styles are set and names of functions and\n        variables are shown. To reproduce the same result as previous versions\n        (<= v1.22.0), please specify `variable_style=None`,\n        `function_style=None`, and `show_name=False` explicitly.\n\n    "
    if (not remove_split):
        raise ValueError('remove_split=False is not supported anymore')
    cands = []
    seen_edges = set()
    nodes = set()
    push_count = [0]

    def add_cand(cand):
        heapq.heappush(cands, ((- cand.rank), push_count[0], cand))
        push_count[0] += 1
    for o in outputs:
        if isinstance(o, variable.Variable):
            o = o.node
        add_cand(o)
        nodes.add(o)
    while cands:
        (_, _, cand) = heapq.heappop(cands)
        if isinstance(cand, variable.VariableNode):
            creator = cand.creator_node
            if ((creator is not None) and ((creator, cand) not in seen_edges)):
                add_cand(creator)
                seen_edges.add((creator, cand))
                nodes.add(creator)
                nodes.add(cand)
        elif isinstance(cand, function_node.FunctionNode):
            for input_ in cand.inputs:
                if ((input_ is not cand) and ((input_, cand) not in seen_edges)):
                    add_cand(input_)
                    seen_edges.add((input_, cand))
                    nodes.add(input_)
                    nodes.add(cand)
    return ComputationalGraph(list(nodes), list(seen_edges), variable_style, function_style, rankdir, remove_variable, show_name)