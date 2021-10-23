

def resize_images(X, height_factor, width_factor, dim_ordering):
    "Resizes the images contained in a 4D tensor of shape\n    - [batch, channels, height, width] (for 'th' dim_ordering)\n    - [batch, height, width, channels] (for 'tf' dim_ordering)\n    by a factor of (height_factor, width_factor). Both factors should be\n    positive integers.\n    "
    if (dim_ordering == 'th'):
        original_shape = int_shape(X)
        new_shape = tf.shape(X)[2:]
        new_shape *= tf.constant(np.array([height_factor, width_factor]).astype('int32'))
        X = permute_dimensions(X, [0, 2, 3, 1])
        X = tf.image.resize_nearest_neighbor(X, new_shape)
        X = permute_dimensions(X, [0, 3, 1, 2])
        X.set_shape((None, None, (original_shape[2] * height_factor), (original_shape[3] * width_factor)))
        return X
    elif (dim_ordering == 'tf'):
        original_shape = int_shape(X)
        new_shape = tf.shape(X)[1:3]
        new_shape *= tf.constant(np.array([height_factor, width_factor]).astype('int32'))
        X = tf.image.resize_nearest_neighbor(X, new_shape)
        X.set_shape((None, (original_shape[1] * height_factor), (original_shape[2] * width_factor), None))
        return X
    else:
        raise Exception(('Invalid dim_ordering: ' + dim_ordering))
