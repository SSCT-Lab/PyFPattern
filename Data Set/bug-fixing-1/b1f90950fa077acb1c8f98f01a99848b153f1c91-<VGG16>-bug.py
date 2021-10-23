

def VGG16(include_top=True, weights='imagenet', input_tensor=None, input_shape=None, pooling=None, classes=1000):
    'Instantiates the VGG16 architecture.\n\n    Optionally loads weights pre-trained\n    on ImageNet. Note that when using TensorFlow,\n    for best performance you should set\n    `image_data_format="channels_last"` in your Keras config\n    at ~/.keras/keras.json.\n\n    The model and the weights are compatible with both\n    TensorFlow and Theano. The data format\n    convention used by the model is the one\n    specified in your Keras config file.\n\n    # Arguments\n        include_top: whether to include the 3 fully-connected\n            layers at the top of the network.\n        weights: one of `None` (random initialization)\n            or "imagenet" (pre-training on ImageNet).\n        input_tensor: optional Keras tensor (i.e. output of `layers.Input()`)\n            to use as image input for the model.\n        input_shape: optional shape tuple, only to be specified\n            if `include_top` is False (otherwise the input shape\n            has to be `(224, 224, 3)` (with `channels_last` data format)\n            or `(3, 224, 224)` (with `channels_first` data format).\n            It should have exactly 3 inputs channels,\n            and width and height should be no smaller than 48.\n            E.g. `(200, 200, 3)` would be one valid value.\n        pooling: Optional pooling mode for feature extraction\n            when `include_top` is `False`.\n            - `None` means that the output of the model will be\n                the 4D tensor output of the\n                last convolutional layer.\n            - `avg` means that global average pooling\n                will be applied to the output of the\n                last convolutional layer, and thus\n                the output of the model will be a 2D tensor.\n            - `max` means that global max pooling will\n                be applied.\n        classes: optional number of classes to classify images\n            into, only to be specified if `include_top` is True, and\n            if no `weights` argument is specified.\n\n    # Returns\n        A Keras model instance.\n\n    # Raises\n        ValueError: in case of invalid argument for `weights`,\n            or invalid input shape.\n    '
    if (weights not in {'imagenet', None}):
        raise ValueError('The `weights` argument should be either `None` (random initialization) or `imagenet` (pre-training on ImageNet).')
    if ((weights == 'imagenet') and include_top and (classes != 1000)):
        raise ValueError('If using `weights` as imagenet with `include_top` as true, `classes` should be 1000')
    input_shape = _obtain_input_shape(input_shape, default_size=224, min_size=48, data_format=K.image_data_format(), include_top=include_top)
    if (input_tensor is None):
        img_input = Input(shape=input_shape)
    elif (not K.is_keras_tensor(input_tensor)):
        img_input = Input(tensor=input_tensor, shape=input_shape)
    else:
        img_input = input_tensor
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv1')(img_input)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', name='block1_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block1_pool')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv1')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', name='block2_conv2')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block2_pool')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv1')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv2')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', name='block3_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block3_pool')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block4_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block4_pool')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv1')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv2')(x)
    x = Conv2D(512, (3, 3), activation='relu', padding='same', name='block5_conv3')(x)
    x = MaxPooling2D((2, 2), strides=(2, 2), name='block5_pool')(x)
    if include_top:
        x = Flatten(name='flatten')(x)
        x = Dense(4096, activation='relu', name='fc1')(x)
        x = Dense(4096, activation='relu', name='fc2')(x)
        x = Dense(classes, activation='softmax', name='predictions')(x)
    elif (pooling == 'avg'):
        x = GlobalAveragePooling2D()(x)
    elif (pooling == 'max'):
        x = GlobalMaxPooling2D()(x)
    if (input_tensor is not None):
        inputs = get_source_inputs(input_tensor)
    else:
        inputs = img_input
    model = Model(inputs, x, name='vgg16')
    if (weights == 'imagenet'):
        if include_top:
            weights_path = get_file('vgg16_weights_tf_dim_ordering_tf_kernels.h5', WEIGHTS_PATH, cache_subdir='models')
        else:
            weights_path = get_file('vgg16_weights_tf_dim_ordering_tf_kernels_notop.h5', WEIGHTS_PATH_NO_TOP, cache_subdir='models')
        model.load_weights(weights_path)
        if (K.backend() == 'theano'):
            layer_utils.convert_all_kernels_in_model(model)
        if (K.image_data_format() == 'channels_first'):
            if include_top:
                maxpool = model.get_layer(name='block5_pool')
                shape = maxpool.output_shape[1:]
                dense = model.get_layer(name='fc1')
                layer_utils.convert_dense_weights_data_format(dense, shape, 'channels_first')
            if (K.backend() == 'tensorflow'):
                warnings.warn('You are using the TensorFlow backend, yet you are using the Theano image data format convention (`image_data_format="channels_first"`). For best performance, set `image_data_format="channels_last"` in your Keras config at ~/.keras/keras.json.')
    return model
