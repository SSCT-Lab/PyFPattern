

@contextlib.contextmanager
@tf_export('xla.experimental.jit_scope')
def experimental_jit_scope(compile_ops=True, separate_compiled_gradients=False):
    "Enable or disable JIT compilation of operators within the scope.\n\n  NOTE: This is an experimental feature.\n\n  The compilation is a hint and only supported on a best-effort basis.\n\n  Example usage:\n\n    ```python\n    with tf.xla.experimental.jit_scope():\n      c = tf.matmul(a, b)  # compiled\n    with tf.xla.experimental.jit_scope(compile_ops=False):\n      d = tf.matmul(a, c)  # not compiled\n    with tf.xla.experimental.jit_scope(\n        compile_ops=lambda node_def: 'matmul' in node_def.op.lower()):\n      e = tf.matmul(a, b) + d  # matmul is compiled, the addition is not.\n    ```\n\n  Example of `separate_compiled_gradients`:\n\n    ```python\n    # In the example below, the computations for f, g and h will all be compiled\n    # in separate scopes.\n    with tf.xla.experimental.jit_scope(\n        separate_compiled_gradients=True):\n      f = tf.matmul(a, b)\n    g = tf.gradients([f], [a, b], name='mygrads1')\n    h = tf.gradients([f], [a, b], name='mygrads2')\n    ```\n\n  Args:\n    compile_ops: Whether to enable or disable compilation in the scope.\n      Either a Python bool, or a callable that accepts the parameter\n      `node_def` and returns a python bool.\n    separate_compiled_gradients: If true put each gradient subgraph into a\n      separate compilation scope. This gives fine-grained control over which\n      portions of the graph will be compiled as a single unit. Compiling\n      gradients separately may yield better performance for some graphs.\n      The scope is named based on the scope of the forward computation as well\n      as the name of the gradients. As a result, the gradients will be compiled\n      in a scope that is separate from both the forward computation, and from\n      other gradients.\n  Raises:\n    RuntimeError: if called when eager execution is enabled.\n  Yields:\n    The current scope, enabling or disabling compilation.\n  "
    if context.executing_eagerly():
        raise RuntimeError('xla.experimental.jit_scope is not supported when eager execution is enabled. Try use it inside tf.function.')
    if callable(compile_ops):

        def xla_compile(node_def):
            return attr_value_pb2.AttrValue(b=compile_ops(node_def))
    else:
        xla_compile = attr_value_pb2.AttrValue(b=compile_ops)
    attrs = {
        '_XlaCompile': xla_compile,
        '_XlaSeparateCompiledGradients': attr_value_pb2.AttrValue(b=bool(separate_compiled_gradients)),
    }
    xla_scope_counter = ops.get_collection(_XLA_SCOPE_KEY)
    if (not xla_scope_counter):
        xla_scope_counter = _XlaScope(0, 0)
        ops.add_to_collection(_XLA_SCOPE_KEY, xla_scope_counter)
    else:
        xla_scope_counter = xla_scope_counter[0]
    if (xla_scope_counter.depth == 0):
        attrs['_XlaScope'] = attr_value_pb2.AttrValue(s=('jit_scope_%d' % xla_scope_counter.count).encode())
        xla_scope_counter.count += 1
    xla_scope_counter.depth += 1
    with ops.get_default_graph()._attr_scope(attrs):
        (yield)
    xla_scope_counter.depth -= 1
