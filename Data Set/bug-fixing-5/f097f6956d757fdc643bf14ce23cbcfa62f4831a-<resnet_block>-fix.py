def resnet_block(inputs, num_filters=16, kernel_size=3, strides=1, activation='relu', batch_normalization=True, conv_first=True):
    '2D Convolution-Batch Normalization-Activation stack builder\n\n    # Arguments\n        inputs (tensor): input tensor from input image or previous layer\n        num_filters (int): Conv2D number of filters\n        kernel_size (int): Conv2D square kernel dimensions\n        strides (int): Conv2D square stride dimensions\n        activation (string): activation name\n        batch_normalization (bool): whether to include batch normalization\n        conv_first (bool): conv-bn-activation (True) or\n            activation-bn-conv (False)\n\n    # Returns\n        x (tensor): tensor as input to the next layer\n    '
    x = inputs
    if conv_first:
        x = Conv2D(num_filters, kernel_size=kernel_size, strides=strides, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(0.0001))(x)
        if batch_normalization:
            x = BatchNormalization()(x)
        if activation:
            x = Activation(activation)(x)
        return x
    if batch_normalization:
        x = BatchNormalization()(x)
    if activation:
        x = Activation('relu')(x)
    x = Conv2D(num_filters, kernel_size=kernel_size, strides=strides, padding='same', kernel_initializer='he_normal', kernel_regularizer=l2(0.0001))(x)
    return x