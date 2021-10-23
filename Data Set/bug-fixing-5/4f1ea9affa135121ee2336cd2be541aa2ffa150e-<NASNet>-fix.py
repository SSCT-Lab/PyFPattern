def NASNet(input_shape=None, penultimate_filters=4032, num_blocks=6, stem_block_filters=96, skip_reduction=True, filter_multiplier=2, include_top=True, weights=None, input_tensor=None, pooling=None, classes=1000, default_size=None):
    "Instantiates a NASNet model.\n\n    Note that only TensorFlow is supported for now,\n    therefore it only works with the data format\n    `image_data_format='channels_last'` in your Keras config\n    at `~/.keras/keras.json`.\n\n    # Arguments\n        input_shape: Optional shape tuple, the input shape\n            is by default `(331, 331, 3)` for NASNetLarge and\n            `(224, 224, 3)` for NASNetMobile.\n            It should have exactly 3 input channels,\n            and width and height should be no smaller than 32.\n            E.g. `(224, 224, 3)` would be one valid value.\n        penultimate_filters: Number of filters in the penultimate layer.\n            NASNet models use the notation `NASNet (N @ P)`, where:\n                -   N is the number of blocks\n                -   P is the number of penultimate filters\n        num_blocks: Number of repeated blocks of the NASNet model.\n            NASNet models use the notation `NASNet (N @ P)`, where:\n                -   N is the number of blocks\n                -   P is the number of penultimate filters\n        stem_block_filters: Number of filters in the initial stem block\n        skip_reduction: Whether to skip the reduction step at the tail\n            end of the network. Set to `False` for CIFAR models.\n        filter_multiplier: Controls the width of the network.\n            - If `filter_multiplier` < 1.0, proportionally decreases the number\n                of filters in each layer.\n            - If `filter_multiplier` > 1.0, proportionally increases the number\n                of filters in each layer.\n            - If `filter_multiplier` = 1, default number of filters from the\n                 paper are used at each layer.\n        include_top: Whether to include the fully-connected\n            layer at the top of the network.\n        weights: `None` (random initialization) or\n            `imagenet` (ImageNet weights)\n        input_tensor: Optional Keras tensor (i.e. output of\n            `layers.Input()`)\n            to use as image input for the model.\n        pooling: Optional pooling mode for feature extraction\n            when `include_top` is `False`.\n            - `None` means that the output of the model\n                will be the 4D tensor output of the\n                last convolutional layer.\n            - `avg` means that global average pooling\n                will be applied to the output of the\n                last convolutional layer, and thus\n                the output of the model will be a\n                2D tensor.\n            - `max` means that global max pooling will\n                be applied.\n        classes: Optional number of classes to classify images\n            into, only to be specified if `include_top` is True, and\n            if no `weights` argument is specified.\n        default_size: Specifies the default image size of the model\n\n    # Returns\n        A Keras model instance.\n\n    # Raises\n        ValueError: In case of invalid argument for `weights`,\n            invalid input shape or invalid `penultimate_filters` value.\n        RuntimeError: If attempting to run this model with a\n            backend that does not support separable convolutions.\n    "
    if (K.backend() in ['cntk', 'theano']):
        raise RuntimeError('Only TensorFlow backend is currently supported, as other backends do not support separable convolution.')
    if (not ((weights in {'imagenet', None}) or os.path.exists(weights))):
        raise ValueError('The `weights` argument should be either `None` (random initialization), `imagenet` (pre-training on ImageNet), or the path to the weights file to be loaded.')
    if ((weights == 'imagenet') and include_top and (classes != 1000)):
        raise ValueError('If using `weights` as ImageNet with `include_top` as true, `classes` should be 1000')
    if (isinstance(input_shape, tuple) and (None in input_shape) and (weights == 'imagenet')):
        raise ValueError((('When specifying the input shape of a NASNet and loading `ImageNet` weights, the input_shape argument must be static (no None entries). Got: `input_shape=' + str(input_shape)) + '`.'))
    if (default_size is None):
        default_size = 331
    input_shape = _obtain_input_shape(input_shape, default_size=default_size, min_size=32, data_format=K.image_data_format(), require_flatten=False, weights=weights)
    if (K.image_data_format() != 'channels_last'):
        warnings.warn('The NASNet family of models is only available for the input data format "channels_last" (width, height, channels). However your settings specify the default data format "channels_first" (channels, width, height). You should set `image_data_format="channels_last"` in your Keras config located at ~/.keras/keras.json. The model being returned right now will expect inputs to follow the "channels_last" data format.')
        K.set_image_data_format('channels_last')
        old_data_format = 'channels_first'
    else:
        old_data_format = None
    if (input_tensor is None):
        img_input = Input(shape=input_shape)
    elif (not K.is_keras_tensor(input_tensor)):
        img_input = Input(tensor=input_tensor, shape=input_shape)
    else:
        img_input = input_tensor
    if ((penultimate_filters % 24) != 0):
        raise ValueError(('For NASNet-A models, the value of `penultimate_filters` needs to be divisible by 24. Current value: %d' % penultimate_filters))
    channel_dim = (1 if (K.image_data_format() == 'channels_first') else (- 1))
    filters = (penultimate_filters // 24)
    if (not skip_reduction):
        x = Conv2D(stem_block_filters, (3, 3), strides=(2, 2), padding='valid', use_bias=False, name='stem_conv1', kernel_initializer='he_normal')(img_input)
    else:
        x = Conv2D(stem_block_filters, (3, 3), strides=(1, 1), padding='same', use_bias=False, name='stem_conv1', kernel_initializer='he_normal')(img_input)
    x = BatchNormalization(axis=channel_dim, momentum=0.9997, epsilon=0.001, name='stem_bn1')(x)
    p = None
    if (not skip_reduction):
        (x, p) = _reduction_a_cell(x, p, (filters // (filter_multiplier ** 2)), block_id='stem_1')
        (x, p) = _reduction_a_cell(x, p, (filters // filter_multiplier), block_id='stem_2')
    for i in range(num_blocks):
        (x, p) = _normal_a_cell(x, p, filters, block_id=('%d' % i))
    (x, p0) = _reduction_a_cell(x, p, (filters * filter_multiplier), block_id=('reduce_%d' % num_blocks))
    p = (p0 if (not skip_reduction) else p)
    for i in range(num_blocks):
        (x, p) = _normal_a_cell(x, p, (filters * filter_multiplier), block_id=('%d' % ((num_blocks + i) + 1)))
    (x, p0) = _reduction_a_cell(x, p, (filters * (filter_multiplier ** 2)), block_id=('reduce_%d' % (2 * num_blocks)))
    p = (p0 if (not skip_reduction) else p)
    for i in range(num_blocks):
        (x, p) = _normal_a_cell(x, p, (filters * (filter_multiplier ** 2)), block_id=('%d' % (((2 * num_blocks) + i) + 1)))
    x = Activation('relu')(x)
    if include_top:
        x = GlobalAveragePooling2D()(x)
        x = Dense(classes, activation='softmax', name='predictions')(x)
    elif (pooling == 'avg'):
        x = GlobalAveragePooling2D()(x)
    elif (pooling == 'max'):
        x = GlobalMaxPooling2D()(x)
    if (input_tensor is not None):
        inputs = get_source_inputs(input_tensor)
    else:
        inputs = img_input
    model = Model(inputs, x, name='NASNet')
    if (weights == 'imagenet'):
        if (default_size == 224):
            if include_top:
                weight_path = NASNET_MOBILE_WEIGHT_PATH
                model_name = 'nasnet_mobile.h5'
            else:
                weight_path = NASNET_MOBILE_WEIGHT_PATH_NO_TOP
                model_name = 'nasnet_mobile_no_top.h5'
            weights_file = get_file(model_name, weight_path, cache_subdir='models')
            model.load_weights(weights_file)
        elif (default_size == 331):
            if include_top:
                weight_path = NASNET_LARGE_WEIGHT_PATH
                model_name = 'nasnet_large.h5'
            else:
                weight_path = NASNET_LARGE_WEIGHT_PATH_NO_TOP
                model_name = 'nasnet_large_no_top.h5'
            weights_file = get_file(model_name, weight_path, cache_subdir='models')
            model.load_weights(weights_file)
        else:
            raise ValueError('ImageNet weights can only be loaded with NASNetLarge or NASNetMobile')
    elif (weights is not None):
        model.load_weights(weights)
    if old_data_format:
        K.set_image_data_format(old_data_format)
    return model