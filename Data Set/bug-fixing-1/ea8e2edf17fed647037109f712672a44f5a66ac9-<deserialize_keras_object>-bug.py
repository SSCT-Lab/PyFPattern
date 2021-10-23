

def deserialize_keras_object(identifier, module_objects=None, custom_objects=None, printable_module_name='object'):
    if isinstance(identifier, dict):
        config = identifier
        if (('class_name' not in config) or ('config' not in config)):
            raise ValueError(('Improper config format: ' + str(config)))
        class_name = config['class_name']
        if (custom_objects and (class_name in custom_objects)):
            cls = custom_objects[class_name]
        elif (class_name in _GLOBAL_CUSTOM_OBJECTS):
            cls = _GLOBAL_CUSTOM_OBJECTS[class_name]
        else:
            module_objects = (module_objects or {
                
            })
            cls = module_objects.get(class_name)
            if (cls is None):
                raise ValueError(((('Unknown ' + printable_module_name) + ': ') + class_name))
        if hasattr(cls, 'from_config'):
            arg_spec = inspect.getargspec(cls.from_config)
            if ('custom_objects' in arg_spec.args):
                custom_objects = (custom_objects or {
                    
                })
                return cls.from_config(config['config'], custom_objects=dict((list(_GLOBAL_CUSTOM_OBJECTS.items()) + list(custom_objects.items()))))
            return cls.from_config(config['config'])
        else:
            return cls(**config['config'])
    elif isinstance(identifier, six.string_types):
        function_name = identifier
        if (custom_objects and (function_name in custom_objects)):
            fn = custom_objects.get(function_name)
        elif (function_name in _GLOBAL_CUSTOM_OBJECTS):
            fn = _GLOBAL_CUSTOM_OBJECTS[function_name]
        else:
            fn = module_objects.get(function_name)
            if (fn is None):
                raise ValueError(('Unknown ' + printable_module_name), (':' + function_name))
        return fn
    else:
        raise ValueError(((('Could not interpret serialized ' + printable_module_name) + ': ') + identifier))
