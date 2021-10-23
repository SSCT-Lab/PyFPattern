def get_attribute_value(attr):
    if (attr.type == AttributeProto.FLOAT):
        return attr.f
    elif (attr.type == AttributeProto.INT):
        return attr.i
    elif (attr.type == AttributeProto.STRING):
        return attr.s
    elif (attr.type == AttributeProto.TENSOR):
        return attr.t
    elif (attr.type == AttributeProto.GRAPH):
        return attr.g
    elif (attr.type == AttributeProto.FLOATS):
        return list(attr.floats)
    elif (attr.type == AttributeProto.INTS):
        return list(attr.ints)
    elif (attr.type == AttributeProto.STRINGS):
        return list(attr.strings)
    elif (attr.type == AttributeProto.TENSORS):
        return list(attr.tensors)
    elif (attr.type == AttributeProto.GRAPHS):
        return list(attr.graphs)
    else:
        raise ValueError('Unsupported ONNX attribute: {}'.format(attr))