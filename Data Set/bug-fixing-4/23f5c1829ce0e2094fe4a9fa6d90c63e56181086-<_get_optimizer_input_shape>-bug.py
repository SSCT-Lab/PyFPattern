def _get_optimizer_input_shape(self, op_type, varkey, orig_shape, param_shape):
    '\n        Returns the shape for optimizer inputs that need to be reshaped when\n        Param and Grad is splited to multiple servers.\n        '
    if (op_type == 'adam'):
        if (varkey in ['Moment1', 'Moment2']):
            return param_shape
    elif (op_type == 'adagrad'):
        if (varkey == 'Moment'):
            return param_shape
    elif (op_type == 'adamax'):
        if (varkey in ['Moment', 'InfNorm']):
            return param_shape
    elif (op_type == 'momentum'):
        if (varkey == 'Velocity'):
            return param_shape
    elif (op_type == ''):
        if (varkey == 'Moment'):
            return param_shape
    elif (op_type == 'sgd'):
        pass
    return orig_shape