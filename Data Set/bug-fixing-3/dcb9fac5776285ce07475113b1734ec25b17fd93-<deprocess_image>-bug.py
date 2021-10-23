def deprocess_image(x):
    if (K.image_dim_ordering() == 'th'):
        x = x.reshape((3, img_width, img_height))
        x = x.transpose((1, 2, 0))
    else:
        x = x.reshape((img_width, img_height, 3))
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    x = x[:, :, ::(- 1)]
    x = np.clip(x, 0, 255).astype('uint8')
    return x