def predict(self, data, batch_size=128, verbose=0):
    'Generates output predictions for the input samples\n        batch by batch.\n\n        Arguments: see `fit` method.\n        '
    x = self._get_x(data)
    output_list = super(Graph, self).predict(x, batch_size=batch_size, verbose=verbose)
    if (not isinstance(output_list, list)):
        output_list = [output_list]
    return dict(zip(self._graph_outputs, output_list))