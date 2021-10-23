def backprop_step(func, target_input_indexes, grad_outputs, grad_inputs):
    'Accumulates gradients of a FunctionNode\n\n    This routine is used by :meth:`chainer.Variable.backward` and\n    :func:`chainer.grad`.\n\n    Args:\n        func (~chainer.FunctionNode): The function for which gradients are\n            accumulated.\n        target_input_indexes (tuple of int): Sorted indices of the inputs\n            that require gradients. It is guaranteed that this tuple contains\n            at least one element.\n        grad_outputs (tuple of Variable): Gradients w.r.t. the output\n            variables. If the gradient w.r.t. an output variable is not\n            given, the corresponding element is ``None``.\n        grad_inputs (dict): References of the gradients w.r.t. the input\n            variables.\n\n    '
    is_debug = chainer.is_debug()
    if is_debug:
        assert isinstance(target_input_indexes, tuple)
        assert (target_input_indexes == tuple(sorted(target_input_indexes)))
        assert isinstance(grad_outputs, tuple)
    if (func.backward_accumulate.__code__ is not chainer.FunctionNode.backward_accumulate.__code__):
        grad_inputs_tuple = tuple([_pop_or_none(grad_inputs[func.inputs[i]]) for i in target_input_indexes])
        gxs = func.backward_accumulate(target_input_indexes, grad_outputs, grad_inputs_tuple)
    else:
        gxs = func.backward(target_input_indexes, grad_outputs)
        if is_debug:
            for gx in gxs:
                if (not ((gx is None) or isinstance(gx, chainer.Variable))):
                    raise ValueError(func._get_error_message('type of gradients returned from backward is incorrect: {} != expected {}'.format(type(gx), chainer.Variable)))
        len_gxs = len(gxs)
        if (len_gxs == len(func.inputs)):
            gxs = tuple([gxs[i] for i in target_input_indexes])
        elif (len_gxs != len(target_input_indexes)):
            msg = 'number of gradients returned from backward is incorrect: '
            if (len(func.inputs) == len(target_input_indexes)):
                msg += ('%s != expected %s' % (len_gxs, len(func.inputs)))
            else:
                msg += ('%s != expected %s or %s' % (len_gxs, len(func.inputs), len(target_input_indexes)))
            raise ValueError(func._get_error_message(msg))
    for (i, gx) in six.moves.zip(target_input_indexes, gxs):
        if (gx is not None):
            grad_inputs[func.inputs[i]].append(gx)
            if is_debug:
                node_x = func.inputs[i]
                g_input_list = grad_inputs[node_x]
                if (gx.shape != node_x.shape):
                    raise ValueError(func._get_error_message('shape of gradients returned from backward is incorrect: input-index={}, actual {} != expected {}'.format(i, gx.shape, node_x.shape)))
                if ((gx is not None) and g_input_list):
                    g_input = g_input_list[0]
                    if (gx.shape != g_input.shape):
                        raise ValueError(func._get_error_message('shape of gradients returned from backward is incorrect: input-index={}, actual {} != expected {}'.format(i, gx.shape, g_input.shape)))
                    if (gx.dtype != g_input.dtype):
                        raise ValueError(func._get_error_message('dtype of gradients returned from backward is incorrect: input-index={}, actual {} != expected {}'.format(i, gx.dtype, g_input.dtype)))
    del gxs
    if is_debug:

        def iter_gxs(gxs):
            for gx in gxs:
                for gx_elem in gx:
                    (yield gx_elem)
        for gx in iter_gxs(grad_inputs.values()):
            if chainer.backend._contains_nan(gx.data):
                raise RuntimeError('NaN is detected on backward computation of {}'.format(func.label))
    if (not func.lazy_grad_sum):
        for gx in grad_inputs.values():
            _reduce(gx)