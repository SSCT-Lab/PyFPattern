def _gen_layer_prototxt(self, layer_params, name='layer', depth=0, indent=2):
    if isinstance(layer_params, (dict, collections.OrderedDict)):
        s = (name + ' {\n')
        indent_s = (' ' * ((depth + 1) * indent))
        for (key, val) in layer_params.items():
            s += (indent_s + self._gen_layer_prototxt(val, name=key, depth=(depth + 1)))
        s += (' ' * (depth * indent))
        s += '}\n'
        return s
    elif isinstance(layer_params, bool):
        return '{}: {}\n'.format(name, ('true' if layer_params else 'false'))
    elif isinstance(layer_params, (six.integer_types + (float,))):
        return '{}: {}\n'.format(name, layer_params)
    elif isinstance(layer_params, str):
        return '{}: "{}"\n'.format(name, layer_params)
    elif isinstance(layer_params, list):
        s = ''
        indent_s = ((' ' * depth) * indent)
        for (i, t) in enumerate(layer_params):
            if (i != 0):
                s += indent_s
            s += self._gen_layer_prototxt(t, name=name, depth=(depth + 1))
        return s
    else:
        raise ValueError(('Unsupported type: ' + str(type(layer_params))))