@tf_export('image.image_gradients')
def image_gradients(image):
    'Returns image gradients (dy, dx) for each color channel.\n\n  Both output tensors have the same shape as the input: [batch_size, h, w,\n  d]. The gradient values are organized so that [I(x+1, y) - I(x, y)] is in\n  location (x, y). That means that dy will always have zeros in the last row,\n  and dx will always have zeros in the last column.\n\n  Arguments:\n    image: Tensor with shape [batch_size, h, w, d].\n\n  Returns:\n    Pair of tensors (dy, dx) holding the vertical and horizontal image\n    gradients (1-step finite difference).\n\n  Usage Example:\n    ```python\n    BATCH_SIZE = 1\n    IMAGE_HEIGHT = 5\n    IMAGE_WIDTH = 5\n    CHANNELS = 1\n    image = tf.reshape(tf.range(IMAGE_HEIGHT * IMAGE_WIDTH * CHANNELS,\n      delta=1, dtype=tf.float32),\n      shape=(BATCH_SIZE, IMAGE_HEIGHT, IMAGE_WIDTH, CHANNELS))\n    dx, dy = tf.image.image_gradients(image)\n    print(image[0, :,:,0])\n    tf.Tensor(\n      [[ 0.  1.  2.  3.  4.]\n      [ 5.  6.  7.  8.  9.]\n      [10. 11. 12. 13. 14.]\n      [15. 16. 17. 18. 19.]\n      [20. 21. 22. 23. 24.]], shape=(5, 5), dtype=float32)\n    print(dx[0, :,:,0])\n    tf.Tensor(\n      [[5. 5. 5. 5. 5.]\n      [5. 5. 5. 5. 5.]\n      [5. 5. 5. 5. 5.]\n      [5. 5. 5. 5. 5.]\n      [0. 0. 0. 0. 0.]], shape=(5, 5), dtype=float32)\n    print(dy[0, :,:,0])\n    tf.Tensor(\n      [[1. 1. 1. 1. 0.]\n      [1. 1. 1. 1. 0.]\n      [1. 1. 1. 1. 0.]\n      [1. 1. 1. 1. 0.]\n      [1. 1. 1. 1. 0.]], shape=(5, 5), dtype=float32)\n    ```\n\n  Raises:\n    ValueError: If `image` is not a 4D tensor.\n  '
    if (image.get_shape().ndims != 4):
        raise ValueError('image_gradients expects a 4D tensor [batch_size, h, w, d], not %s.', image.get_shape())
    image_shape = array_ops.shape(image)
    (batch_size, height, width, depth) = array_ops.unstack(image_shape)
    dy = (image[:, 1:, :, :] - image[:, :(- 1), :, :])
    dx = (image[:, :, 1:, :] - image[:, :, :(- 1), :])
    shape = array_ops.stack([batch_size, 1, width, depth])
    dy = array_ops.concat([dy, array_ops.zeros(shape, image.dtype)], 1)
    dy = array_ops.reshape(dy, image_shape)
    shape = array_ops.stack([batch_size, height, 1, depth])
    dx = array_ops.concat([dx, array_ops.zeros(shape, image.dtype)], 2)
    dx = array_ops.reshape(dx, image_shape)
    return (dy, dx)