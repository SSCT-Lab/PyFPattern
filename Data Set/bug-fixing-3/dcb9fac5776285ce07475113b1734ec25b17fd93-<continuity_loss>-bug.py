def continuity_loss(x):
    assert (K.ndim(x) == 4)
    if (K.image_dim_ordering() == 'th'):
        a = K.square((x[:, :, :(img_width - 1), :(img_height - 1)] - x[:, :, 1:, :(img_height - 1)]))
        b = K.square((x[:, :, :(img_width - 1), :(img_height - 1)] - x[:, :, :(img_width - 1), 1:]))
    else:
        a = K.square((x[:, :(img_width - 1), :(img_height - 1), :] - x[:, 1:, :(img_height - 1), :]))
        b = K.square((x[:, :(img_width - 1), :(img_height - 1), :] - x[:, :(img_width - 1), 1:, :]))
    return K.sum(K.pow((a + b), 1.25))