@mx_op.register('max')
def convert_max(node, **kwargs):
    "Map MXNet's max operator attributes to onnx's ReduceMax operator\n    and return the created node.\n    "
    (name, input_nodes, attrs) = get_inputs(node, kwargs)
    mx_axis = attrs.get('axis', None)
    axes = (convert_string_to_list(str(mx_axis)) if (mx_axis is not None) else None)
    keepdims = get_boolean_attribute_value(attrs, 'keepdims')
    if (axes is not None):
        node = onnx.helper.make_node('ReduceMax', inputs=input_nodes, outputs=[name], axes=axes, keepdims=keepdims, name=name)
        return [node]
    else:
        node = onnx.helper.make_node('ReduceMax', inputs=input_nodes, outputs=[name], keepdims=keepdims, name=name)
        return [node]