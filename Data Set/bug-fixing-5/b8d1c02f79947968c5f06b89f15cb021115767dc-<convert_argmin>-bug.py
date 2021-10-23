@mx_op.register('argmin')
def convert_argmin(node, **kwargs):
    "Map MXNet's argmin operator attributes to onnx's ArgMin operator\n    and return the created node.\n    "
    (name, input_nodes, attrs) = get_inputs(node, kwargs)
    axis = int(attrs.get('axis'))
    keepdims = (int(attrs.get('keepdims')) if ('keepdims' in attrs) else 1)
    node = onnx.helper.make_node('ArgMin', inputs=input_nodes, axis=axis, keepdims=keepdims, outputs=[name], name=name)
    return [node]