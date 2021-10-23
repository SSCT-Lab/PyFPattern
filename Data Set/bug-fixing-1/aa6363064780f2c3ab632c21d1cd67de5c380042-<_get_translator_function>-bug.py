

def _get_translator_function(layer_type):
    'Get the right translator function\n    '
    if (layer_type in _LAYER_REGISTERY):
        return _LAYER_REGISTERY[layer_type]
    else:
        raise TypeError(('Shape computation function missing for layer of type %s.' % type(layer_type)))
