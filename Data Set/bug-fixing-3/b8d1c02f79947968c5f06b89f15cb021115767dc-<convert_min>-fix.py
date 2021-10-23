@mx_op.register('min')
def convert_min(node, **kwargs):
    "Map MXNet's min operator attributes to onnx's ReduceMin operator\n    and return the created node.\n    "
    (name, input_nodes, attrs) = get_inputs(node, kwargs)
    mx_axis = attrs.get('axis', None)
    axes = (convert_string_to_list(str(mx_axis)) if (mx_axis is not None) else None)
    keepdims = get_boolean_attribute_value(attrs, 'keepdims')
    if (axes is not None):
        node = onnx.helper.make_node('ReduceMin', inputs=input_nodes, outputs=[name], axes=axes, keepdims=keepdims, name=name)
        return [node]
    else:
        node = onnx.helper.make_node('ReduceMin', inputs=input_nodes, outputs=[name], keepdims=keepdims, name=name)
        return [node]