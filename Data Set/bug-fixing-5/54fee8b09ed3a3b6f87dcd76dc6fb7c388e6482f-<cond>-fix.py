@tf_export('cond')
@deprecation.deprecated_args(None, 'fn1/fn2 are deprecated in favor of the true_fn/false_fn arguments.', 'fn1', 'fn2')
def cond(pred, true_fn=None, false_fn=None, strict=False, name=None, fn1=None, fn2=None):
    "Return `true_fn()` if the predicate `pred` is true else `false_fn()`.\n\n  `true_fn` and `false_fn` both return lists of output tensors. `true_fn` and\n  `false_fn` must have the same non-zero number and type of outputs.\n\n  Note that the conditional execution applies only to the operations defined in\n  `true_fn` and `false_fn`. Consider the following simple program:\n\n  ```python\n  z = tf.multiply(a, b)\n  result = tf.cond(x < y, lambda: tf.add(x, z), lambda: tf.square(y))\n  ```\n\n  If `x < y`, the `tf.add` operation will be executed and `tf.square`\n  operation will not be executed. Since `z` is needed for at least one\n  branch of the `cond`, the `tf.multiply` operation is always executed,\n  unconditionally.\n  Although this behavior is consistent with the dataflow model of TensorFlow,\n  it has occasionally surprised some users who expected a lazier semantics.\n\n  Note that `cond` calls `true_fn` and `false_fn` *exactly once* (inside the\n  call to `cond`, and not at all during `Session.run()`). `cond`\n  stitches together the graph fragments created during the `true_fn` and\n  `false_fn` calls with some additional graph nodes to ensure that the right\n  branch gets executed depending on the value of `pred`.\n\n  `tf.cond` supports nested structures as implemented in\n  `tensorflow.python.util.nest`. Both `true_fn` and `false_fn` must return the\n  same (possibly nested) value structure of lists, tuples, and/or named tuples.\n  Singleton lists and tuples form the only exceptions to this: when returned by\n  `true_fn` and/or `false_fn`, they are implicitly unpacked to single values.\n  This behavior is disabled by passing `strict=True`.\n\n  Args:\n    pred: A scalar determining whether to return the result of `true_fn` or\n      `false_fn`.\n    true_fn: The callable to be performed if pred is true.\n    false_fn: The callable to be performed if pred is false.\n    strict: A boolean that enables/disables 'strict' mode; see above.\n    name: Optional name prefix for the returned tensors.\n\n  Returns:\n    Tensors returned by the call to either `true_fn` or `false_fn`. If the\n    callables return a singleton list, the element is extracted from the list.\n\n  Raises:\n    TypeError: if `true_fn` or `false_fn` is not callable.\n    ValueError: if `true_fn` and `false_fn` do not return the same number of\n      tensors, or return tensors of different types.\n\n  Example:\n\n  ```python\n  x = tf.constant(2)\n  y = tf.constant(5)\n  def f1(): return tf.multiply(x, 17)\n  def f2(): return tf.add(y, 23)\n  r = tf.cond(tf.less(x, y), f1, f2)\n  # r is set to f1().\n  # Operations in f2 (e.g., tf.add) are not executed.\n  ```\n\n  "
    if _ENABLE_COND_V2:
        return cond_v2_impl.cond_v2(pred, true_fn, false_fn, name)
    if (fn1 is not None):
        if (true_fn is not None):
            raise TypeError('cond(): true_fn and fn1 may not be set simultaneously.')
        true_fn = fn1
    elif (true_fn is None):
        raise TypeError('cond(): true_fn argument required')
    if (fn2 is not None):
        if (false_fn is not None):
            raise TypeError('cond(): false_fn and fn2 may not be set simultaneously.')
        false_fn = fn2
    elif (false_fn is None):
        raise TypeError('cond(): false_fn argument required')
    if (not callable(true_fn)):
        raise TypeError('true_fn must be callable.')
    if (not callable(false_fn)):
        raise TypeError('false_fn must be callable.')
    with ops.name_scope(name, 'cond', [pred]):
        if context.executing_eagerly():
            if pred:
                return _UnpackIfSingleton(true_fn())
            return _UnpackIfSingleton(false_fn())
        if isinstance(pred, bool):
            raise TypeError('pred must not be a Python bool')
        (p_2, p_1) = switch(pred, pred)
        pivot_1 = array_ops.identity(p_1, name='switch_t')
        pivot_2 = array_ops.identity(p_2, name='switch_f')
        pred = array_ops.identity(pred, name='pred_id')
        for tensor in [p_1, p_2, pivot_1, pivot_2, pred]:
            tensor.op.graph.prevent_fetching(tensor.op)
        context_t = CondContext(pred, pivot_1, branch=1)
        try:
            context_t.Enter()
            (orig_res_t, res_t) = context_t.BuildCondBranch(true_fn)
            if (orig_res_t is None):
                raise ValueError('true_fn must have a return value.')
            context_t.ExitResult(res_t)
        finally:
            context_t.Exit()
        context_f = CondContext(pred, pivot_2, branch=0)
        try:
            context_f.Enter()
            (orig_res_f, res_f) = context_f.BuildCondBranch(false_fn)
            if (orig_res_f is None):
                raise ValueError('false_fn must have a return value.')
            context_f.ExitResult(res_f)
        finally:
            context_f.Exit()
        if (not strict):
            orig_res_t = _UnpackIfSingleton(orig_res_t)
            orig_res_f = _UnpackIfSingleton(orig_res_f)
        try:
            nest.assert_same_structure(orig_res_t, orig_res_f)
        except TypeError as e:
            raise TypeError('Incompatible return types of true_fn and false_fn: {}'.format(e))
        except ValueError as e:
            raise ValueError('Incompatible return values of true_fn and false_fn: {}'.format(e))
        if (not res_t):
            raise ValueError('true_fn and false_fn must return at least one result.')
        res_t_flat = nest.flatten(res_t)
        res_f_flat = nest.flatten(res_f)
        for (x, y) in zip(res_t_flat, res_f_flat):
            assert ((isinstance(x, ops.IndexedSlices) and isinstance(y, ops.IndexedSlices)) or (isinstance(x, sparse_tensor.SparseTensor) and isinstance(y, sparse_tensor.SparseTensor)) or (isinstance(x, ops.Tensor) and isinstance(y, ops.Tensor)))
            val_x = (x if isinstance(x, ops.Tensor) else x.values)
            val_y = (y if isinstance(y, ops.Tensor) else y.values)
            if (val_x.dtype.base_dtype != val_y.dtype.base_dtype):
                raise ValueError(('Outputs of true_fn and false_fn must have the same type: %s, %s' % (val_x.dtype.name, val_y.dtype.name)))
        merges = [merge(pair)[0] for pair in zip(res_f_flat, res_t_flat)]
        merges = _convert_flows_to_tensorarrays(nest.flatten(orig_res_t), merges)
        assert (context_t.outer_context == context_f.outer_context)
        if (context_t.outer_context is None):
            ops.add_to_collection(ops.GraphKeys.COND_CONTEXT, context_t)
            ops.add_to_collection(ops.GraphKeys.COND_CONTEXT, context_f)
        merges = nest.pack_sequence_as(structure=orig_res_t, flat_sequence=merges)
        if (not strict):
            merges = _UnpackIfSingleton(merges)
        return merges