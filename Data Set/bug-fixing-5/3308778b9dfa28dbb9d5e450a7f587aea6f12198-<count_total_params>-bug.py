def count_total_params(layers, layer_set=None):
    "Counts the number of parameters in a list of layers.\n\n    # Arguments\n        layers: list of layers.\n        layer_set: set of layers already seen\n            (so that we don't count their weights twice).\n\n    # Returns\n        A tuple (count of trainable weights, count of non-trainable weights.)\n    "
    if (layer_set is None):
        layer_set = set()
    trainable_count = 0
    non_trainable_count = 0
    for layer in layers:
        if (layer in layer_set):
            continue
        layer_set.add(layer)
        if hasattr(layer, 'layers'):
            (t, nt) = count_total_params(layer.layers, layer_set)
            trainable_count += t
            non_trainable_count += nt
        else:
            trainable_count += np.sum([K.count_params(p) for p in layer.trainable_weights])
            non_trainable_count += np.sum([K.count_params(p) for p in layer.non_trainable_weights])
    return (trainable_count, non_trainable_count)