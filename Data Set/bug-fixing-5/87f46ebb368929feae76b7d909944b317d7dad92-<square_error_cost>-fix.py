def square_error_cost(input, label, **kwargs):
    "\n    **Square error cost layer**\n\n    This layer accepts input predictions and target label and returns the squared error cost.\n    For predictions, :math:`X`, and target labels, :math:`Y`, the equation is:\n\n    .. math::\n\n        Out = (X - Y)^2\n\n    In the above equation:\n\n        * :math:`X`: Input predictions, a tensor.\n        * :math:`Y`: Input labels, a tensor.\n        * :math:`Out`: Output value, same shape with :math:`X`.\n\n    Args:\n       input(Variable): Input tensor, has predictions.\n       label(Variable): Label tensor, has target labels.\n\n    Returns:\n        Variable: The tensor variable storing the element-wise squared error difference                   of input and label.\n\n    Examples:\n        .. code-block:: python\n\n          y = layers.data(name='y', shape=[1], dtype='float32')\n          y_predict = layers.data(name='y_predict', shape=[1], dtype='float32')\n          cost = layers.square_error_cost(input=y_predict, label=y)\n\n    "
    helper = LayerHelper('square_error_cost', **kwargs)
    minus_out = helper.create_tmp_variable(dtype=input.dtype)
    helper.append_op(type='elementwise_sub', inputs={
        'X': [input],
        'Y': [label],
    }, outputs={
        'Out': [minus_out],
    })
    square_out = helper.create_tmp_variable(dtype=input.dtype)
    helper.append_op(type='square', inputs={
        'X': [minus_out],
    }, outputs={
        'Out': [square_out],
    })
    return square_out