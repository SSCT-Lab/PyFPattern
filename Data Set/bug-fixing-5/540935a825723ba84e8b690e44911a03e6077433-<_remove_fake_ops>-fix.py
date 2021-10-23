def _remove_fake_ops(self, graph):
    for op in graph.all_op_nodes():
        if (op.name() in self._fake_quantize_types):
            op_out = graph._find_node_by_name(op.outputs, op.output('Out')[0])
            next_op = op_out.outputs[0]
            if (next_op.name() not in self._mul_ops):
                self._remove_fake_quantize(graph, op)
    for op in graph.all_op_nodes():
        if (op.name() in self._fake_dequantize_types):
            op_in = graph._find_node_by_name(op.inputs, op.input('X')[0])
            prev_op = op_in.inputs[0]
            if (prev_op.name() not in self._mul_ops):
                self._remove_fake_dequantize(graph, op)
    return graph