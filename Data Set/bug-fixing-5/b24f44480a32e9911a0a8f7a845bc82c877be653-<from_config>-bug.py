@classmethod
def from_config(cls, config, custom_objects=None):
    globs = globals()
    if custom_objects:
        globs = dict((list(globs.items()) + list(custom_objects.items())))
    function_type = config.pop('function_type')
    if (function_type == 'function'):
        function = deserialize_keras_object(config['function'], custom_objects=custom_objects, printable_module_name='function in Lambda layer')
    elif (function_type == 'lambda'):
        function = func_load(config['function'], globs=globs)
    else:
        raise TypeError('Unknown function type:', function_type)
    output_shape_type = config.pop('output_shape_type')
    if (output_shape_type == 'function'):
        output_shape = deserialize_keras_object(config['output_shape'], custom_objects=custom_objects, printable_module_name='output_shape function in Lambda layer')
    elif (output_shape_type == 'lambda'):
        output_shape = func_load(config['output_shape'], globs=globs)
    else:
        output_shape = config['output_shape']
    if ('arguments' in config):
        for key in config['arguments']:
            if isinstance(config['arguments'][key], dict):
                arg_dict = config['arguments'][key]
                if (('type' in arg_dict) and (arg_dict['type'] == 'ndarray')):
                    config['arguments'][key] = np.array(arg_dict['value'])
    config['function'] = function
    config['output_shape'] = output_shape
    return cls(**config)