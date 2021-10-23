def add_input_distortions(flip_left_right, random_crop, random_scale, random_brightness):
    "Creates the operations to apply the specified distortions.\n\n  During training it can help to improve the results if we run the images\n  through simple distortions like crops, scales, and flips. These reflect the\n  kind of variations we expect in the real world, and so can help train the\n  model to cope with natural data more effectively. Here we take the supplied\n  parameters and construct a network of operations to apply them to an image.\n\n  Cropping\n  ~~~~~~~~\n\n  Cropping is done by placing a bounding box at a random position in the full\n  image. The cropping parameter controls the size of that box relative to the\n  input image. If it's zero, then the box is the same size as the input and no\n  cropping is performed. If the value is 50%, then the crop box will be half the\n  width and height of the input. In a diagram it looks like this:\n\n  <       width         >\n  +---------------------+\n  |                     |\n  |   width - crop%     |\n  |    <      >         |\n  |    +------+         |\n  |    |      |         |\n  |    |      |         |\n  |    |      |         |\n  |    +------+         |\n  |                     |\n  |                     |\n  +---------------------+\n\n  Scaling\n  ~~~~~~~\n\n  Scaling is a lot like cropping, except that the bounding box is always\n  centered and its size varies randomly within the given range. For example if\n  the scale percentage is zero, then the bounding box is the same size as the\n  input and no scaling is applied. If it's 50%, then the bounding box will be in\n  a random range between half the width and height and full size.\n\n  Args:\n    flip_left_right: Boolean whether to randomly mirror images horizontally.\n    random_crop: Integer percentage setting the total margin used around the\n    crop box.\n    random_scale: Integer percentage of how much to vary the scale by.\n    random_brightness: Integer range to randomly multiply the pixel values by.\n    graph.\n\n  Returns:\n    The jpeg input layer and the distorted result tensor.\n  "
    jpeg_data = tf.placeholder(tf.string, name='DistortJPGInput')
    decoded_image = tf.image.decode_jpeg(jpeg_data)
    decoded_image_as_float = tf.cast(decoded_image, dtype=tf.float32)
    decoded_image_4d = tf.expand_dims(decoded_image_as_float, 0)
    margin_scale = (1.0 + (random_crop / 100.0))
    resize_scale = (1.0 + (random_scale / 100.0))
    margin_scale_value = tf.constant(margin_scale)
    resize_scale_value = tf.random_uniform(tensor_shape.scalar(), minval=1.0, maxval=resize_scale)
    scale_value = tf.mul(margin_scale_value, resize_scale_value)
    precrop_width = tf.mul(scale_value, MODEL_INPUT_WIDTH)
    precrop_height = tf.mul(scale_value, MODEL_INPUT_HEIGHT)
    precrop_shape = tf.pack([precrop_height, precrop_width])
    precrop_shape_as_int = tf.cast(precrop_shape, dtype=tf.int32)
    precropped_image = tf.image.resize_bilinear(decoded_image_4d, precrop_shape_as_int)
    precropped_image_3d = tf.squeeze(precropped_image, squeeze_dims=[0])
    cropped_image = tf.random_crop(precropped_image_3d, [MODEL_INPUT_HEIGHT, MODEL_INPUT_WIDTH, MODEL_INPUT_DEPTH])
    if flip_left_right:
        flipped_image = tf.image.random_flip_left_right(cropped_image)
    else:
        flipped_image = cropped_image
    brightness_min = (1.0 - (random_brightness / 100.0))
    brightness_max = (1.0 + (random_brightness / 100.0))
    brightness_value = tf.random_uniform(tensor_shape.scalar(), minval=brightness_min, maxval=brightness_max)
    brightened_image = tf.mul(flipped_image, brightness_value)
    distort_result = tf.expand_dims(brightened_image, 0, name='DistortResult')
    return (jpeg_data, distort_result)