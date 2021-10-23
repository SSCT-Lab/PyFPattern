

@mx_op.register('dot')
def convert_dot(node, **kwargs):
    "Map MXNet's dot operator attributes to onnx's\n    MatMul and Transpose operators based on the values set for\n    transpose_a, transpose_b attributes."
    (name, input_nodes, attrs) = get_inputs(node, kwargs)
    trans_a_node = None
    trans_b_node = None
    trans_a = get_boolean_attribute_value(attrs, 'transpose_a')
    trans_b = get_boolean_attribute_value(attrs, 'transpose_b')
    op_name = ('transpose' + str(kwargs['idx']))
    if trans_a:
        trans_a_node = create_helper_trans_node(op_name, input_nodes[0], 'a')
        input_node_a = (op_name + '_a')
    if trans_b:
        trans_b_node = create_helper_trans_node(op_name, input_nodes[1], 'b')
        input_node_b = (op_name + '_b')
    matmul_node = onnx.helper.make_node('MatMul', inputs=[input_node_a, input_node_b], outputs=[name], name=name)
    if ((not trans_a) and (not trans_b)):
        return [matmul_node]
    elif (trans_a and (not trans_b)):
        return [trans_a_node, matmul_node]
    elif (trans_b and (not trans_a)):
        return [trans_b_node, matmul_node]
    else:
        return [trans_a_node, trans_b_node, matmul_node]
