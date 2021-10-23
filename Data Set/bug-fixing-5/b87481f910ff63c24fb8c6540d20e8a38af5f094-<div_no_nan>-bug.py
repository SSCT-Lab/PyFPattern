@tf_export('math.divide_no_nan', v1=['math.divide_no_nan', 'div_no_nan'])
@deprecation.deprecated_endpoints('div_no_nan')
@dispatch.add_dispatch_support
def div_no_nan(x, y, name=None):
    'Computes an unsafe divide which returns 0 if the y is zero.\n\n  Args:\n    x: A `Tensor`. Must be one of the following types: `float32`, `float64`.\n    y: A `Tensor` whose dtype is compatible with `x`.\n    name: A name for the operation (optional).\n\n  Returns:\n    The element-wise value of the x divided by y.\n  '
    with ops.name_scope(name, 'div_no_nan', [x, y]) as name:
        x = ops.convert_to_tensor(x, name='x', dtype=x.dtype.base_dtype)
        y = ops.convert_to_tensor(y, name='y')
        return gen_math_ops.div_no_nan(x, y, name=name)