def make_model(dense_layer_sizes, nb_filters, nb_conv, nb_pool):
    'Creates model comprised of 2 convolutional layers followed by dense layers\n\n    dense_layer_sizes: List of layer sizes. This list has one number for each layer\n    nb_filters: Number of convolutional filters in each convolutional layer\n    nb_conv: Convolutional kernel size\n    nb_pool: Size of pooling area for max pooling\n    '
    model = Sequential()
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv, border_mode='valid', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Convolution2D(nb_filters, nb_conv, nb_conv))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(nb_pool, nb_pool)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    for layer_size in dense_layer_sizes:
        model.add(Dense(layer_size))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    return model