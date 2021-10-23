def calculate_gain(nonlinearity, param=None):
    "Return the recommended gain value for the given nonlinearity function.\n    The values are as follows:\n\n    ============ ==========================================\n    nonlinearity gain\n    ============ ==========================================\n    linear       :math:`1`\n    conv{1,2,3}d :math:`1`\n    sigmoid      :math:`1`\n    tanh         :math:`5 / 3`\n    relu         :math:`\\sqrt{2}`\n    leaky_relu   :math:`\\sqrt{2 / (1 + negative\\_slope^2)}`\n    ============ ==========================================\n\n    Args:\n        nonlinearity: the nonlinear function (`nn.functional` name)\n        param: optional parameter for the nonlinear function\n\n    Examples:\n        >>> gain = nn.init.gain('leaky_relu')\n    "
    linear_fns = ['linear', 'conv1d', 'conv2d', 'conv3d', 'conv_transpose1d', 'conv_transpose2d', 'conv_transpose3d']
    if ((nonlinearity in linear_fns) or (nonlinearity == 'sigmoid')):
        return 1
    elif (nonlinearity == 'tanh'):
        return (5.0 / 3)
    elif (nonlinearity == 'relu'):
        return math.sqrt(2.0)
    elif (nonlinearity == 'leaky_relu'):
        if (param is None):
            negative_slope = 0.01
        elif (((not isinstance(param, bool)) and isinstance(param, int)) or isinstance(param, float)):
            negative_slope = param
        else:
            raise ValueError('negative_slope {} not a valid number'.format(param))
        return math.sqrt((2.0 / (1 + (negative_slope ** 2))))
    else:
        raise ValueError('Unsupported nonlinearity {}'.format(nonlinearity))