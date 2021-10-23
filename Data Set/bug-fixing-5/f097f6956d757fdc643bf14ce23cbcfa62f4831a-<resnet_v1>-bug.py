def resnet_v1(input_shape, depth, num_classes=10):
    'ResNet Version 1 Model builder [a]\n\n    Stacks of 2 x (3 x 3) Conv2D-BN-ReLU\n    Last ReLU is after the shortcut connection.\n    The number of filters doubles when the feature maps size\n    is halved.\n    The Number of parameters is approx the same as Table 6 of [a]:\n    ResNet20 0.27M\n    ResNet32 0.46M\n    ResNet44 0.66M\n    ResNet56 0.85M\n    ResNet110 1.7M\n\n    # Arguments\n        input_shape (tensor): shape of input image tensor\n        depth (int): number of core convolutional layers\n        num_classes (int): number of classes (CIFAR10 has 10)\n\n    # Returns\n        model (Model): Keras model instance\n    '
    if (((depth - 2) % 6) != 0):
        raise ValueError('depth should be 6n+2 (eg 20, 32, 44 in [a])')
    inputs = Input(shape=input_shape)
    num_filters = 16
    num_sub_blocks = int(((depth - 2) / 6))
    x = resnet_block(inputs=inputs)
    for i in range(3):
        for j in range(num_sub_blocks):
            strides = 1
            is_first_layer_but_not_first_block = ((j == 0) and (i > 0))
            if is_first_layer_but_not_first_block:
                strides = 2
            y = resnet_block(inputs=x, num_filters=num_filters, strides=strides)
            y = resnet_block(inputs=y, num_filters=num_filters, activation=None)
            if is_first_layer_but_not_first_block:
                x = resnet_block(inputs=x, num_filters=num_filters, kernel_size=1, strides=strides, activation=None)
            x = keras.layers.add([x, y])
            x = Activation('relu')(x)
        num_filters = (2 * num_filters)
    x = AveragePooling2D(pool_size=8)(x)
    y = Flatten()(x)
    outputs = Dense(num_classes, activation='softmax', kernel_initializer='he_normal')(y)
    model = Model(inputs=inputs, outputs=outputs)
    return model