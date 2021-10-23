def region_style_loss(style_image, target_image, style_mask, target_mask):
    'Calculate style loss between style_image and target_image,\n    for one common region specified by their (boolean) masks\n    '
    assert (3 == K.ndim(style_image) == K.ndim(target_image))
    assert (2 == K.ndim(style_mask) == K.ndim(target_mask))
    if (K.image_data_format() == 'channels_first'):
        masked_style = (style_image * style_mask)
        masked_target = (target_image * target_mask)
        num_channels = K.shape(style_image)[0]
    else:
        masked_style = (K.permute_dimensions(style_image, (2, 0, 1)) * style_mask)
        masked_target = (K.permute_dimensions(target_image, (2, 0, 1)) * target_mask)
        num_channels = K.shape(style_image)[(- 1)]
    num_channels = K.cast(num_channels, dtype='float32')
    s = ((gram_matrix(masked_style) / K.mean(style_mask)) / num_channels)
    c = ((gram_matrix(masked_target) / K.mean(target_mask)) / num_channels)
    return K.mean(K.square((s - c)))