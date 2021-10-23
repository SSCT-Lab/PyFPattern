

def make_model(dense_layer_sizes, filters, kernel_size, pool_size):
    'Creates model comprised of 2 convolutional layers followed by dense layers\n\n    dense_layer_sizes: List of layer sizes.\n        This list has one number for each layer\n    filters: Number of convolutional filters in each convolutional layer\n    kernel_size: Convolutional kernel size\n    pool_size: Size of pooling area for max pooling\n    '
    model = Sequential()
    model.add(Conv2D(filters, kernel_size, padding='valid', input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(Conv2D(filters, kernel_size))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.25))
    model.add(Flatten())
    for layer_size in dense_layer_sizes:
        model.add(Dense(layer_size))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
    return model
