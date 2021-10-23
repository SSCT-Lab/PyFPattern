def get_attribute_value(attr):
    if attr.HasField('f'):
        return attr.f
    elif attr.HasField('i'):
        return attr.i
    elif attr.HasField('s'):
        return attr.s
    elif attr.HasField('t'):
        return attr.t
    elif attr.HasField('g'):
        return attr.g
    elif len(attr.floats):
        return list(attr.floats)
    elif len(attr.ints):
        return list(attr.ints)
    elif len(attr.strings):
        return list(attr.strings)
    elif len(attr.tensors):
        return list(attr.tensors)
    elif len(attr.graphs):
        return list(attr.graphs)
    else:
        raise ValueError('Unsupported ONNX attribute: {}'.format(attr))