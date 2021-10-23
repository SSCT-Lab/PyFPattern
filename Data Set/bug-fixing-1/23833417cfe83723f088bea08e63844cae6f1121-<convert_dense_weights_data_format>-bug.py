

def convert_dense_weights_data_format(dense, previous_feature_map_shape, target_data_format='channels_first'):
    'Utility useful when changing a convnet\'s `data_format`.\n\n    When porting the weights of a convnet from one data format to the other,\n    if the convnet includes a `Flatten` layer\n    (applied to the last convolutional feature map)\n    followed by a `Dense` layer, the weights of that `Dense` layer\n    should be updated to reflect the new dimension ordering.\n\n    # Arguments\n        dense: The target `Dense` layer.\n        previous_feature_map_shape: A shape tuple of 3 integers,\n            e.g. `(512, 7, 7)`. The shape of the convolutional\n            feature map right before the `Flatten` layer that\n            came before the target `Dense` layer.\n        target_data_format: One of "channels_last", "channels_first".\n            Set it "channels_last"\n            if converting a "chnnels_first" model to "channels_last",\n            or reciprocally.\n    '
    assert (target_data_format in {'channels_last', 'channels_first'})
    (kernel, bias) = dense.get_weights()
    for i in range(kernel.shape[1]):
        if (target_data_format == 'channels_first'):
            (c, h, w) = previous_feature_map_shape
            original_fm_shape = (h, w, c)
            ki = kernel[:, i].reshape(original_fm_shape)
            ki = np.transpose(ki, (2, 0, 1))
        else:
            (h, w, c) = previous_feature_map_shape
            original_fm_shape = (c, h, w)
            ki = kernel[:, i].reshape(original_fm_shape)
            ki = np.transpose(ki, (1, 2, 0))
        kernel[:, i] = np.reshape(ki, (np.prod(previous_feature_map_shape),))
    dense.set_weights([kernel, bias])
