def resnet_v2(input_shape, depth, num_classes=10):
    'ResNet Version 2 Model builder [b]\n\n    Stacks of (1 x 1)-(3 x 3)-(1 x 1) BN-ReLU-Conv2D or also known as\n    bottleneck layer\n    First shortcut connection per layer is 1 x 1 Conv2D.\n    Second and onwards shortcut connection is identity.\n    Features maps sizes: 16(input), 64(1st sub_block), 128(2nd), 256(3rd)\n\n    # Arguments\n        input_shape (tensor): shape of input image tensor\n        depth (int): number of core convolutional layers\n        num_classes (int): number of classes (CIFAR10 has 10)\n\n    # Returns\n        model (Model): Keras model instance\n    '
    if (((depth - 2) % 9) != 0):
        raise ValueError('depth should be 9n+2 (eg 56 or 110 in [b])')
    inputs = Input(shape=input_shape)
    num_filters_in = 16
    num_filters_out = 64
    filter_multiplier = 4
    num_sub_blocks = int(((depth - 2) / 9))
    x = Conv2D(num_filters_in, kernel_size=3, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(0.0001))(inputs)
    for i in range(3):
        if (i > 0):
            filter_multiplier = 2
        num_filters_out = (num_filters_in * filter_multiplier)
        for j in range(num_sub_blocks):
            strides = 1
            is_first_layer_but_not_first_block = ((j == 0) and (i > 0))
            if is_first_layer_but_not_first_block:
                strides = 2
            y = resnet_block(inputs=x, num_filters=num_filters_in, kernel_size=1, strides=strides, conv_first=False)
            y = resnet_block(inputs=y, num_filters=num_filters_in, conv_first=False)
            y = resnet_block(inputs=y, num_filters=num_filters_out, kernel_size=1, conv_first=False)
            if (j == 0):
                x = Conv2D(num_filters_out, kernel_size=1, strides=strides, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(0.0001))(x)
            x = keras.layers.add([x, y])
        num_filters_in = num_filters_out
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = AveragePooling2D(pool_size=8)(x)
    y = Flatten()(x)
    outputs = Dense(num_classes, activation='softmax', kernel_initializer='he_normal')(y)
    model = Model(inputs=inputs, outputs=outputs)
    return model