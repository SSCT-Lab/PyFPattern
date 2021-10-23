

def cond(pred, fn1, fn2, name=None):
    'Return either fn1() or fn2() based on the boolean predicate `pred`.\n\n  `fn1` and `fn2` both return lists of output tensors. `fn1` and `fn2` must have\n  the same non-zero number and type of outputs.\n\n  Note that the conditional execution applies only to the operations defined in\n  fn1 and fn2. Consider the following simple program:\n\n  ```python\n  z = tf.mul(a, b)\n  result = tf.cond(x < y, lambda: tf.add(x, z), lambda: tf.square(y))\n  ```\n\n  If x < y, the `tf.add` operation will be executed and tf.square\n  operation will not be executed. Since z is needed for at least one\n  branch of the cond, the tf.mul operation is always executed, unconditionally.\n  Although this behavior is consistent with the dataflow model of TensorFlow,\n  it has occasionally surprised some users who expected a lazier semantics.\n\n  Args:\n    pred: A scalar determining whether to return the result of `fn1` or `fn2`.\n    fn1: The callable to be performed if pred is true.\n    fn2: The callable to be performed if pref is false.\n    name: Optional name prefix for the returned tensors.\n\n  Returns:\n    Tensors returned by the call to either `fn1` or `fn2`. If the callables\n    return a singleton list, the element is extracted from the list.\n\n  Raises:\n    TypeError: if `fn1` or `fn2` is not callable.\n    ValueError: if `fn1` and `fn2` do not return the same number of tensors, or\n                return tensors of different types.\n\n  Example:\n\n  ```python\n    x = tf.constant(2)\n    y = tf.constant(5)\n    def f1(): return tf.mul(x, 17)\n    def f2(): return tf.add(y, 23)\n    r = tf.cond(tf.less(x, y), f1, f2)\n    # r is set to f1().\n    # Operations in f2 (e.g., tf.add) are not executed.\n  ```\n\n  '
    with ops.name_scope(name, 'cond', [pred]) as name:
        if (not callable(fn1)):
            raise TypeError('fn1 must be callable.')
        if (not callable(fn2)):
            raise TypeError('fn2 must be callable.')
        if isinstance(pred, bool):
            raise TypeError('pred must not be a Python bool')
        (p_2, p_1) = switch(pred, pred)
        pivot_1 = array_ops.identity(p_1, name='switch_t')
        pivot_2 = array_ops.identity(p_2, name='switch_f')
        pred = array_ops.identity(pred, name='pred_id')
        for tensor in [p_1, p_2, pivot_1, pivot_2, pred]:
            tensor.op.graph.prevent_fetching(tensor.op)
        context_t = CondContext(pred, pivot_1, branch=1)
        context_t.Enter()
        (orig_res, res_t) = context_t.BuildCondBranch(fn1)
        context_t.ExitResult(res_t)
        context_t.Exit()
        context_f = CondContext(pred, pivot_2, branch=0)
        context_f.Enter()
        (_, res_f) = context_f.BuildCondBranch(fn2)
        context_f.ExitResult(res_f)
        context_f.Exit()
        if (len(res_t) != len(res_f)):
            raise ValueError('fn1 and fn2 must return the same number of results.')
        if (not res_t):
            raise ValueError('fn1 and fn2 must return at least one result.')
        for (x, y) in zip(res_f, res_t):
            assert ((isinstance(x, ops.IndexedSlices) and isinstance(y, ops.IndexedSlices)) or (isinstance(x, sparse_tensor.SparseTensor) and isinstance(y, sparse_tensor.SparseTensor)) or (isinstance(x, ops.Tensor) and isinstance(y, ops.Tensor)))
            val_x = (x if isinstance(x, ops.Tensor) else x.values)
            val_y = (y if isinstance(y, ops.Tensor) else y.values)
            if (val_x.dtype.base_dtype != val_y.dtype.base_dtype):
                raise ValueError(('Outputs of fn1 and fn2 must have the same type: %s, %s' % (val_x.dtype.name, val_y.dtype.name)))
        merges = [merge([x[0], x[1]])[0] for x in zip(res_f, res_t)]
        merges = _convert_flows_to_tensorarrays(orig_res, merges)
        ops.add_to_collection(ops.GraphKeys.COND_CONTEXT, context_t)
        ops.add_to_collection(ops.GraphKeys.COND_CONTEXT, context_f)
        return (merges[0] if (len(merges) == 1) else merges)
