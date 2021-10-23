def get_attribute_value(attr):
    if (attr.type is AttributeProto.FLOAT):
        return attr.f
    elif (attr.type is AttributeProto.INT):
        return attr.i
    elif (attr.type is AttributeProto.STRING):
        return attr.s
    elif (attr.type is AttributeProto.TENSOR):
        return attr.t
    elif (attr.type is AttributeProto.GRAPH):
        return attr.g
    elif (attr.type is AttributeProto.FLOATS):
        return list(attr.floats)
    elif (attr.type is AttributeProto.INTS):
        return list(attr.ints)
    elif (attr.type is AttributeProto.STRINGS):
        return list(attr.strings)
    elif (attr.type is AttributeProto.TENSORS):
        return list(attr.tensors)
    elif (attr.type is AttributeProto.GRAPHS):
        return list(attr.graphs)
    else:
        raise ValueError('Unsupported ONNX attribute: {}'.format(attr))