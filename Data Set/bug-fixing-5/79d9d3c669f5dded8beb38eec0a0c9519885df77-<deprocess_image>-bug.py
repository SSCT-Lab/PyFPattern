def deprocess_image(x):
    x -= x.mean()
    x /= (x.std() + K.epsilon())
    x *= 0.1
    x += 0.5
    x = np.clip(x, 0, 1)
    x *= 255
    if (K.image_data_format() == 'channels_first'):
        x = x.transpose((1, 2, 0))
    x = np.clip(x, 0, 255).astype('uint8')
    return x