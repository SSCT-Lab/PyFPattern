

def pool3d(x, pool_size, strides=(1, 1, 1), padding='valid', data_format=None, pool_mode='max'):
    if (data_format is None):
        data_format = image_data_format()
    if (data_format not in {'channels_first', 'channels_last'}):
        raise ValueError('Unknown data_format:', data_format)
    if (padding == 'same'):
        w_pad = ((pool_size[0] - 2) if ((pool_size[0] % 2) == 1) else (pool_size[0] - 1))
        h_pad = ((pool_size[1] - 2) if ((pool_size[1] % 2) == 1) else (pool_size[1] - 1))
        d_pad = ((pool_size[2] - 2) if ((pool_size[2] % 2) == 1) else (pool_size[2] - 1))
        pad = (w_pad, h_pad, d_pad)
    elif (padding == 'valid'):
        pad = (0, 0, 0)
    else:
        raise ValueError('Invalid padding:', padding)
    if (data_format == 'channels_last'):
        x = x.dimshuffle((0, 4, 1, 2, 3))
    if (pool_mode == 'max'):
        pool_out = pool.pool_3d(x, ws=pool_size, stride=strides, ignore_border=True, pad=pad, mode='max')
    elif (pool_mode == 'avg'):
        pool_out = pool.pool_3d(x, ws=pool_size, stride=strides, ignore_border=True, pad=pad, mode='average_exc_pad')
    else:
        raise ValueError('Invalid pooling mode:', pool_mode)
    if (padding == 'same'):
        expected_width = (((x.shape[2] + strides[0]) - 1) // strides[0])
        expected_height = (((x.shape[3] + strides[1]) - 1) // strides[1])
        expected_depth = (((x.shape[4] + strides[2]) - 1) // strides[2])
        pool_out = pool_out[:, :, :expected_width, :expected_height, :expected_depth]
    if (data_format == 'channels_last'):
        pool_out = pool_out.dimshuffle((0, 2, 3, 4, 1))
    return pool_out
