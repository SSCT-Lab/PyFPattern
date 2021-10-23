def square_error_cost(input, label, **kwargs):
    '\n    This functions returns the squared error cost using the input and label.\n    The output is appending the op to do the above.\n    '
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