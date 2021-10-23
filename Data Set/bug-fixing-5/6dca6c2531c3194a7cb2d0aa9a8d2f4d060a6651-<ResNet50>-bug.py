def ResNet50(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000):
    'Instantiates the ResNet50 architecture.\n\n    Optionally loads weights pre-trained\n    on ImageNet. Note that when using TensorFlow,\n    for best performance you should set\n    `image_data_format="channels_last"` in your Keras config\n    at ~/.keras/keras.json.\n\n    The model and the weights are compatible with both\n    TensorFlow and Theano. The data format\n    convention used by the model is the one\n    specified in your Keras config file.\n\n    # Arguments\n        include_top: whether to include the 3 fully-connected\n            layers at the top of the network.\n        weights: one of `None` (random initialization)\n            or "imagenet" (pre-training on ImageNet).\n        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)\n            to use as image input for the model.\n        input_shape: optional shape tuple, only to be specified\n            if `include_top` is False (otherwise the input shape\n            has to be `(224, 224, 3)` (with `channels_last` data format)\n            or `(3, 224, 244)` (with `channels_first` data format).\n            It should have exactly 3 inputs channels,\n            and width and height should be no smaller than 197.\n            E.g. `(200, 200, 3)` would be one valid value.\n        pooling: Optional pooling mode for feature extraction\n            when `include_top` is `False`.\n            - `None` means that the output of the model will be\n                the 4D tensor output of the\n                last convolutional layer.\n            - `avg` means that global average pooling\n                will be applied to the output of the\n                last convolutional layer, and thus\n                the output of the model will be a 2D tensor.\n            - `max` means that global max pooling will\n                be applied.\n        classes: optional number of classes to classify images\n            into, only to be specified if `include_top` is True, and\n            if no `weights` argument is specified.\n\n    # Returns\n        A Keras model instance.\n\n    # Raises\n        ValueError: in case of invalid argument for `weights`,\n            or invalid input shape.\n    '
    if (weights not in {'imagenet', None}):
        raise ValueError('The `weights` argument should be either `None` (random initialization) or `imagenet` (pre-training on ImageNet).')
    if ((weights == 'imagenet') and include_top and (classes != 1000)):
        raise ValueError('If using `weights` as imagenet with `include_top` as true, `classes` should be 1000')
    input_shape = _obtain_input_shape(input_shape, default_size=224, min_size=197, data_format=K.image_data_format(), include_top=include_top)
    if (input_tensor is None):
        img_input = Input(shape=input_shape)
    elif (not K.is_keras_tensor(input_tensor)):
        img_input = Input(tensor=input_tensor, shape=input_shape)
    else:
        img_input = input_tensor
    if (K.image_data_format() == 'channels_last'):
        bn_axis = 3
    else:
        bn_axis = 1
    x = ZeroPadding2D((3, 3))(img_input)
    x = Conv2D(64, (7, 7), strides=(2, 2), name='conv1')(x)
    x = BatchNormalization(axis=bn_axis, name='bn_conv1')(x)
    x = Activation('relu')(x)
    x = MaxPooling2D((3, 3), strides=(2, 2))(x)
    x = conv_block(x, 3, [64, 64, 256], stage=2, block='a', strides=(1, 1))
    x = identity_block(x, 3, [64, 64, 256], stage=2, block='b')
    x = identity_block(x, 3, [64, 64, 256], stage=2, block='c')
    x = conv_block(x, 3, [128, 128, 512], stage=3, block='a')
    x = identity_block(x, 3, [128, 128, 512], stage=3, block='b')
    x = identity_block(x, 3, [128, 128, 512], stage=3, block='c')
    x = identity_block(x, 3, [128, 128, 512], stage=3, block='d')
    x = conv_block(x, 3, [256, 256, 1024], stage=4, block='a')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='b')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='c')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='d')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='e')
    x = identity_block(x, 3, [256, 256, 1024], stage=4, block='f')
    x = conv_block(x, 3, [512, 512, 2048], stage=5, block='a')
    x = identity_block(x, 3, [512, 512, 2048], stage=5, block='b')
    x = identity_block(x, 3, [512, 512, 2048], stage=5, block='c')
    x = AveragePooling2D((7, 7), name='avg_pool')(x)
    if include_top:
        x = Flatten()(x)
        x = Dense(classes, activation='softmax', name='fc1000')(x)
    elif (pooling == 'avg'):
        x = GlobalAveragePooling2D()(x)
    elif (pooling == 'max'):
        x = GlobalMaxPooling2D()(x)
    if (input_tensor is not None):
        inputs = get_source_inputs(input_tensor)
    else:
        inputs = img_input
    model = Model(inputs, x, name='resnet50')
    if (weights == 'imagenet'):
        if include_top:
            weights_path = get_file('resnet50_weights_tf_dim_ordering_tf_kernels.h5', WEIGHTS_PATH, cache_subdir='models', md5_hash='a7b3fe01876f51b976af0dea6bc144eb')
        else:
            weights_path = get_file('resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5', WEIGHTS_PATH_NO_TOP, cache_subdir='models', md5_hash='a268eb855778b3df3c7506639542a6af')
        model.load_weights(weights_path)
        if (K.backend() == 'theano'):
            layer_utils.convert_all_kernels_in_model(model)
        if (K.image_data_format() == 'channels_first'):
            if include_top:
                maxpool = model.get_layer(name='avg_pool')
                shape = maxpool.output_shape[1:]
                dense = model.get_layer(name='fc1000')
                layer_utils.convert_dense_weights_data_format(dense, shape, 'channels_first')
            if (K.backend() == 'tensorflow'):
                warnings.warn('You are using the TensorFlow backend, yet you are using the Theano image data format convention (`image_data_format="channels_first"`). For best performance, set `image_data_format="channels_last"` in your Keras config at ~/.keras/keras.json.')
    return model