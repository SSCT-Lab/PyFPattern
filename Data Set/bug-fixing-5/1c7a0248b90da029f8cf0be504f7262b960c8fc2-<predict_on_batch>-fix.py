def predict_on_batch(self, data):
    output_list = super(Graph, self).predict_on_batch(data)
    if (not isinstance(output_list, list)):
        output_list = [output_list]
    return dict(zip(self._graph_outputs, output_list))