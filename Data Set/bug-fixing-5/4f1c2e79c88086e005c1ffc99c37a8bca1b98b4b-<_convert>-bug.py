def _convert(model, input_names=None, output_names=None, image_input_names=None, is_bgr=False, red_bias=0.0, green_bias=0.0, blue_bias=0.0, gray_bias=0.0, image_scale=1.0, class_labels=None, predicted_feature_name=None, predicted_probabilities_output=''):
    if (_keras.backend.image_data_format() == 'channels_first'):
        print("Keras image data format 'channels_first' detected. Currently only 'channels_last' is supported. Changing to 'channels_last', but your model may not be converted converted properly.")
        _keras.backend.set_image_data_format('channels_last')
    if isinstance(model, _string_types):
        model = _keras.models.load_model(model)
    elif isinstance(model, tuple):
        model = _load_keras_model(model[0], model[1])
    _check_unsupported_layers(model)
    graph = _topology2.NetGraph(model)
    graph.build()
    graph.generate_blob_names()
    graph.add_recurrent_optionals()
    inputs = graph.get_input_layers()
    outputs = graph.get_output_layers()
    if (input_names is not None):
        if isinstance(input_names, _string_types):
            input_names = [input_names]
    else:
        input_names = [('input' + str((i + 1))) for i in range(len(inputs))]
    if (output_names is not None):
        if isinstance(output_names, _string_types):
            output_names = [output_names]
    else:
        output_names = [('output' + str((i + 1))) for i in range(len(outputs))]
    if ((image_input_names is not None) and isinstance(image_input_names, _string_types)):
        image_input_names = [image_input_names]
    graph.reset_model_input_names(input_names)
    graph.reset_model_output_names(output_names)
    if (type(model.input_shape) is list):
        input_dims = [filter(None, x) for x in model.input_shape]
        unfiltered_shapes = model.input_shape
    else:
        input_dims = [filter(None, model.input_shape)]
        unfiltered_shapes = [model.input_shape]
    for (idx, dim) in enumerate(input_dims):
        unfiltered_shape = unfiltered_shapes[idx]
        dim = list(dim)
        if (len(dim) == 0):
            input_dims[idx] = tuple([1])
        elif (len(dim) == 1):
            s = graph.get_successors(inputs[idx])[0]
            if isinstance(graph.get_keras_layer(s), _keras.layers.embeddings.Embedding):
                input_dims[idx] = (1,)
            else:
                input_dims[idx] = dim
        elif (len(dim) == 2):
            input_dims[idx] = (dim[1],)
        elif (len(dim) == 3):
            if (len(unfiltered_shape) > 3):
                input_dims[idx] = (dim[2], dim[0], dim[1])
            else:
                input_dims[idx] = (dim[2],)
        else:
            raise ValueError(("Input '%s' has input shape of length %d" % (input_names[idx], len(dim))))
    if (type(model.output_shape) is list):
        output_dims = [filter(None, x) for x in model.output_shape]
    else:
        output_dims = [filter(None, model.output_shape[1:])]
    for (idx, dim) in enumerate(output_dims):
        dim = list(dim)
        if (len(dim) == 1):
            output_dims[idx] = dim
        elif (len(dim) == 2):
            output_dims[idx] = (dim[1],)
        elif (len(dim) == 3):
            output_dims[idx] = (dim[2], dim[1], dim[0])
    input_types = [datatypes.Array(*dim) for dim in input_dims]
    output_types = [datatypes.Array(*dim) for dim in output_dims]
    input_names = map(str, input_names)
    output_names = map(str, output_names)
    is_classifier = (class_labels is not None)
    if is_classifier:
        mode = 'classifier'
    else:
        mode = None
    input_features = list(zip(input_names, input_types))
    output_features = list(zip(output_names, output_types))
    builder = _NeuralNetworkBuilder(input_features, output_features, mode=mode)
    for (iter, layer) in enumerate(graph.layer_list):
        keras_layer = graph.keras_layer_map[layer]
        print(('%d : %s, %s' % (iter, layer, keras_layer)))
        if isinstance(keras_layer, _keras.layers.wrappers.TimeDistributed):
            keras_layer = keras_layer.layer
        converter_func = _get_layer_converter_fn(keras_layer)
        (input_names, output_names) = graph.get_layer_blobs(layer)
        converter_func(builder, layer, input_names, output_names, keras_layer)
    builder.add_optionals(graph.optional_inputs, graph.optional_outputs)
    if is_classifier:
        classes_in = class_labels
        if isinstance(classes_in, _string_types):
            import os
            if (not os.path.isfile(classes_in)):
                raise ValueError(('Path to class labels (%s) does not exist.' % classes_in))
            with open(classes_in, 'r') as f:
                classes = f.read()
            classes = classes.splitlines()
        elif (type(classes_in) is list):
            classes = classes_in
        else:
            raise ValueError('Class labels must be a list of integers / strings, or a file path')
        if (predicted_feature_name is not None):
            builder.set_class_labels(classes, predicted_feature_name=predicted_feature_name, prediction_blob=predicted_probabilities_output)
        else:
            builder.set_class_labels(classes)
    builder.set_pre_processing_parameters(image_input_names=image_input_names, is_bgr=is_bgr, red_bias=red_bias, green_bias=green_bias, blue_bias=blue_bias, gray_bias=gray_bias, image_scale=image_scale)
    spec = builder.spec
    return _MLModel(spec)