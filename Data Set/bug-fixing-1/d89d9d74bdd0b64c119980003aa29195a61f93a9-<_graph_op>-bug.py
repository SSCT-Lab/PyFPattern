

def _graph_op(g, opname, *raw_args, **kwargs):
    "\n    Create an ONNX operator 'opname', taking 'args' as inputs and attributes\n    'kwargs'; returning the node representing the single output of this operator\n    (see the `outputs` keyword argument for multi-return nodes).\n\n    The set of operators and the inputs/attributes they take\n    is documented at https://github.com/onnx/onnx/blob/master/docs/Operators.md\n\n    This function is monkey-patched onto Graph.\n\n    Arguments:\n        opname (string): The ONNX operator name, e.g., `Abs` or `Add`.\n        args (Node...): The inputs to the operator; usually provided\n            as arguments to the `symbolic` definition.\n        kwargs: The attributes of the ONNX operator, with keys named\n            according to the following convention: `alpha_f` indicates\n            the `alpha` attribute with type `f`.  The valid type specifiers are\n            `f` (float), `i` (int), `s` (string) or `t` (Tensor).  An attribute\n            specified with type float accepts either a single float, or a\n            list of floats (e.g., you would say `dims_i` for a `dims` attribute\n            that takes a list of integers).\n        outputs (int, optional):  The number of outputs this operator returns;\n            by default an operator is assumed to return a single output.\n            If `outputs` is greater than one, this functions returns a tuple\n            of output `Node`, representing each output of the ONNX operator\n            in positional.\n    "
    outputs = kwargs.pop('outputs', 1)
    kwargs = dict(((k, v) for (k, v) in kwargs.iteritems() if (v is not None)))

    def const_if_tensor(arg):
        if isinstance(arg, torch._C.Node):
            return arg
        else:
            return g.op('Constant', value_z=arg)
    args = list((const_if_tensor(arg) for arg in raw_args))
    n = g.appendNode(_newNode(g, opname, *args, **kwargs))
    if (outputs == 1):
        return n
    return tuple((g.appendNode(g.createSelect(n, i)) for i in _range(outputs)))
