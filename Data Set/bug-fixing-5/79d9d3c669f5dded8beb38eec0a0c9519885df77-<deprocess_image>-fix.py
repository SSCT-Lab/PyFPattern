def deprocess_image(x):
    'utility function to convert a float array into a valid uint8 image.\n\n    # Arguments\n        x: A numpy-array representing the generated image.\n\n    # Returns\n        A processed numpy-array, which could be used in e.g. imshow.\n    '
    x -= x.mean()
    x /= (x.std() + K.epsilon())
    x *= 0.25
    x += 0.5
    x = np.clip(x, 0, 1)
    x *= 255
    if (K.image_data_format() == 'channels_first'):
        x = x.transpose((1, 2, 0))
    x = np.clip(x, 0, 255).astype('uint8')
    return x