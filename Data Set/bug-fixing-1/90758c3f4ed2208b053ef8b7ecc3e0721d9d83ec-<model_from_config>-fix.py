

def model_from_config(config, custom_objects=None):
    'Instantiates a Keras model from its config.\n\n    # Arguments\n        config: Configuration dictionary.\n        custom_objects: Optional dictionary mapping names\n            (strings) to custom classes or functions to be\n            considered during deserialization.\n\n    # Returns\n        A Keras model instance (uncompiled).\n    '
    if isinstance(config, list):
        raise TypeError('`model_from_config` expects a dictionary, not a list. Maybe you meant to use `Sequential.from_config(config)`?')
    return layer_module.deserialize(config, custom_objects=custom_objects)
