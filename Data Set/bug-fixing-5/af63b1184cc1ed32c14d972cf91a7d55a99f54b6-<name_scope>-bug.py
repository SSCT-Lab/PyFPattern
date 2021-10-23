@signature_safe_contextmanager
def name_scope(prefix=None):
    '\n    Generate hierarchical name prefix for the operators.\n\n    Note: This should only used for debugging and visualization purpose.\n    Don\'t use it for serious analysis such as graph/program transformations.\n\n    Args:\n        prefix(str): prefix.\n\n    Examples:\n        .. code-block:: python\n\n          import paddle.fluid as fluid\n          with fluid.name_scope("s1"):\n              a = fluid.layers.data(name=\'data\', shape=[1], dtype=\'int32\')\n              b = a + 1\n              with fluid.name_scope("s2"):\n                  c = b * 1\n              with fluid.name_scope("s3"):\n                  d = c / 1\n          with fluid.name_scope("s1"):\n              f = fluid.layers.pow(d, 2.0)\n          with fluid.name_scope("s4"):\n              g = f - 1\n    '
    assert prefix, 'namescope prefix cannot be empty.'
    global _name_scope
    _name_scope = _name_scope.child(prefix)
    (yield)
    _name_scope = _name_scope.parent()