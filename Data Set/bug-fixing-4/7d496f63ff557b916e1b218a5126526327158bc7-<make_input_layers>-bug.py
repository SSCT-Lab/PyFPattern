def make_input_layers(self):
    '\n        Extract the ordering of the input layers. \n        '
    self.input_layers = []
    if hasattr(self.model, 'input_layers'):
        input_keras_layers = self.model.input_layers[:]
        self.input_layers = ([None] * len(input_keras_layers))
        for layer in self.layer_list:
            keras_layer = self.keras_layer_map[layer]
            if isinstance(keras_layer, _keras.engine.topology.InputLayer):
                if (keras_layer in input_keras_layers):
                    idx = input_keras_layers.index(keras_layer)
                    self.input_layers[idx] = layer
    elif (len(self.model.inbound_nodes) <= 1):
        for ts in _to_list(self.model.input):
            for l in self.layer_list:
                kl = self.keras_layer_map[l]
                if (isinstance(kl, _keras.engine.topology.InputLayer) and (kl.input == ts)):
                    self.input_layers.append(l)
    else:
        raise ValueError('Input values cannot be identified.')