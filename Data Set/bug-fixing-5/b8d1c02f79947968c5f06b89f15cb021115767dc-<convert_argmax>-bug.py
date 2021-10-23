@mx_op.register('argmax')
def convert_argmax(node, **kwargs):
    "Map MXNet's argmax operator attributes to onnx's ArgMax operator\n    and return the created node.\n    "
    (name, input_nodes, attrs) = get_inputs(node, kwargs)
    axis = int(attrs.get('axis'))
    keepdims = (int(attrs.get('keepdims')) if ('keepdims' in attrs) else 1)
    node = onnx.helper.make_node('ArgMax', inputs=input_nodes, axis=axis, keepdims=keepdims, outputs=[name], name=name)
    return [node]