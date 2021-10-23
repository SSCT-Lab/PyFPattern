def predict_on_batch(self, data):
    output_list = super(Graph, self).predict_on_batch(data)
    return dict(zip(self._graph_outputs, output_list))