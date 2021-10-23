

@K.eager
def set_weights(self, weights):
    "Sets the weights of the layer, from Numpy arrays.\n\n        # Arguments\n            weights: a list of Numpy arrays. The number\n                of arrays and their shape must match\n                number of the dimensions of the weights\n                of the layer (i.e. it should match the\n                output of `get_weights`).\n\n        # Raises\n            ValueError: If the provided weights list does not match the\n                layer's specifications.\n        "
    params = self.weights
    if (len(params) != len(weights)):
        raise ValueError((((((((('You called `set_weights(weights)` on layer "' + self.name) + '" with a  weight list of length ') + str(len(weights))) + ', but the layer was expecting ') + str(len(params))) + ' weights. Provided weights: ') + str(weights)[:50]) + '...'))
    if (not params):
        return
    weight_value_tuples = []
    param_values = K.batch_get_value(params)
    for (pv, p, w) in zip(param_values, params, weights):
        if (pv.shape != w.shape):
            raise ValueError(((('Layer weight shape ' + str(pv.shape)) + ' not compatible with provided weight shape ') + str(w.shape)))
        weight_value_tuples.append((p, w))
    K.batch_set_value(weight_value_tuples)
