

def to_categorical(y, nb_classes=None):
    'Convert class vector (integers from 0 to nb_classes) to binary class matrix, for use with categorical_crossentropy.\n\n    # Arguments\n        y: class vector to be converted into a matrix\n        nb_classes: total number of classes\n\n    # Returns\n        A binary matrix representation of the input.\n    '
    y = np.array(y, dtype='int')
    if (not nb_classes):
        nb_classes = (np.max(y) + 1)
    Y = np.zeros((len(y), nb_classes))
    for i in range(len(y)):
        Y[(i, y[i])] = 1.0
    return Y
