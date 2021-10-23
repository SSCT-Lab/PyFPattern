def merge(inputs, mode='sum', concat_axis=(- 1), dot_axes=(- 1), output_shape=None, name=None):
    "Functional merge, to apply to Keras tensors (NOT layers).\n    Returns a Keras tensor.\n\n    # Example usage:\n\n    ```python\n    tensor_a = Input(shape=(32,))\n    tensor_b = Input(shape=(32,))\n    merged_tensor = merge([tensor_a, tensor_b], mode='concat', concat_axis=1)\n    ```\n\n    # Arguments\n        mode: string or lambda/function. If string, must be one\n            of: 'sum', 'mul', 'concat', 'ave', 'cos', 'dot'.\n            If lambda/function, it should take as input a list of tensors\n            and return a single tensor.\n        concat_axis: integer, axis to use in mode `concat`.\n        dot_axes: integer or tuple of integers, axes to use in mode `dot`.\n        output_shape: shape tuple (tuple of integers), or lambda/function\n            to compute output_shape (only if merge mode is a lambda/function).\n            If the latter case, it should take as input a list of shape tuples\n            (1:1 mapping to input tensors) and return a single shape tuple.\n        node_indices: optional list of integers containing\n            the output node index for each input layer\n            (in case some input layers have multiple output nodes).\n            will default to an array of 0s if not provided.\n        tensor_indices: optional list of indices of output tensors\n            to consider for merging\n            (in case some input layer node returns multiple tensors).\n    "
    all_keras_tensors = True
    for x in inputs:
        if (not hasattr(x, '_keras_history')):
            all_keras_tensors = False
            break
    if all_keras_tensors:
        input_layers = []
        node_indices = []
        tensor_indices = []
        for x in inputs:
            (input_layer, node_index, tensor_index) = x._keras_history
            input_layers.append(input_layer)
            node_indices.append(node_index)
            tensor_indices.append(tensor_index)
        merge_layer = Merge(input_layers, mode=mode, concat_axis=concat_axis, dot_axes=dot_axes, output_shape=output_shape, node_indices=node_indices, tensor_indices=tensor_indices, name=name)
        return merge_layer.inbound_nodes[0].output_tensors[0]
    else:
        merge_layer = Merge(mode=mode, concat_axis=concat_axis, dot_axes=dot_axes, output_shape=output_shape, name=name)
        return merge_layer(inputs)