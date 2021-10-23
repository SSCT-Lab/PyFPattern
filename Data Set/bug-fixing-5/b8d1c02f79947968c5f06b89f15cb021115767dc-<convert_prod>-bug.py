@mx_op.register('prod')
def convert_prod(node, **kwargs):
    "Map MXNet's prod operator attributes to onnx's ReduceProd operator\n    and return the created node.\n    "
    (name, input_nodes, attrs) = get_inputs(node, kwargs)
    mx_axis = attrs.get('axis', None)
    axes = (convert_string_to_list(str(mx_axis)) if (mx_axis is not None) else None)
    keepdims = int(attrs.get('keepdims', 0))
    if (axes is not None):
        node = onnx.helper.make_node('ReduceProd', inputs=input_nodes, outputs=[name], axes=axes, keepdims=keepdims, name=name)
        return [node]
    else:
        node = onnx.helper.make_node('ReduceProd', inputs=input_nodes, outputs=[name], keepdims=keepdims, name=name)
        return [node]