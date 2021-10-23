

@tf_export('image.per_image_standardization')
def per_image_standardization(image):
    "Linearly scales `image` to have zero mean and unit norm.\n\n  This op computes `(x - mean) / adjusted_stddev`, where `mean` is the average\n  of all values in image, and\n  `adjusted_stddev = max(stddev, 1.0/sqrt(image.NumElements()))`.\n\n  `stddev` is the standard deviation of all values in `image`. It is capped\n  away from zero to protect against division by 0 when handling uniform images.\n\n  Args:\n    image: 3-D tensor of shape `[height, width, channels]`.\n\n  Returns:\n    The standardized image with same shape as `image`.\n\n  Raises:\n    ValueError: if the shape of 'image' is incompatible with this function.\n  "
    with ops.name_scope(None, 'per_image_standardization', [image]) as scope:
        image = ops.convert_to_tensor(image, name='image')
        image = _Assert3DImage(image)
        num_pixels = math_ops.reduce_prod(array_ops.shape(image))
        image = math_ops.cast(image, dtype=dtypes.float32)
        image_mean = math_ops.reduce_mean(image)
        variance = (math_ops.reduce_mean(math_ops.square(image)) - math_ops.square(image_mean))
        variance = gen_nn_ops.relu(variance)
        stddev = math_ops.sqrt(variance)
        min_stddev = math_ops.rsqrt(math_ops.cast(num_pixels, dtypes.float32))
        pixel_value_scale = math_ops.maximum(stddev, min_stddev)
        pixel_value_offset = image_mean
        image = math_ops.subtract(image, pixel_value_offset)
        image = math_ops.div(image, pixel_value_scale, name=scope)
        return image
