@classmethod
def from_config(cls, config):
    function_type = config.pop('function_type')
    if (function_type == 'function'):
        function = globals()[config['function']]
    elif (function_type == 'lambda'):
        function = marshal.loads(config['function'].encode('raw_unicode_escape'))
        function = python_types.FunctionType(function, globals())
    else:
        raise Exception(('Unknown function type: ' + function_type))
    output_shape_type = config.pop('output_shape_type')
    if (output_shape_type == 'function'):
        output_shape = globals()[config['output_shape']]
    elif (output_shape_type == 'lambda'):
        output_shape = marshal.loads(config['output_shape'].encode('raw_unicode_escape'))
        output_shape = python_types.FunctionType(output_shape, globals())
    else:
        output_shape = config['output_shape']
    config['function'] = function
    config['output_shape'] = output_shape
    return cls(**config)