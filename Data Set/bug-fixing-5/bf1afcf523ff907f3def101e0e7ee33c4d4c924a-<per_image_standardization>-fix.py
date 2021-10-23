@tf_export('image.per_image_standardization')
def per_image_standardization(image):
    "Linearly scales each image in `image` to have mean 0 and variance 1.\n\n  For each 3-D image `x` in `image`, computes `(x - mean) / adjusted_stddev`,\n  where\n\n  - `mean` is the average of all values in `x`\n  - `adjusted_stddev = max(stddev, 1.0/sqrt(N))` is capped away from 0 to\n    protect against division by 0 when handling uniform images\n    - `N` is the number of elements in `x`\n    - `stddev` is the standard deviation of all values in `x`\n\n  Args:\n    image: An n-D Tensor with at least 3 dimensions, the last 3 of which are the\n      dimensions of each image.\n\n  Returns:\n    A `Tensor` with the same shape and dtype as `image`.\n\n  Raises:\n    ValueError: if the shape of 'image' is incompatible with this function.\n  "
    with ops.name_scope(None, 'per_image_standardization', [image]) as scope:
        image = ops.convert_to_tensor(image, name='image')
        image = _AssertAtLeast3DImage(image)
        orig_dtype = image.dtype
        if (orig_dtype not in [dtypes.float16, dtypes.float32]):
            image = convert_image_dtype(image, dtypes.float32)
        num_pixels = math_ops.reduce_prod(array_ops.shape(image)[(- 3):])
        image_mean = math_ops.reduce_mean(image, axis=[(- 1), (- 2), (- 3)], keepdims=True)
        stddev = math_ops.reduce_std(image, axis=[(- 1), (- 2), (- 3)], keepdims=True)
        min_stddev = math_ops.rsqrt(math_ops.cast(num_pixels, image.dtype))
        adjusted_stddev = math_ops.maximum(stddev, min_stddev)
        image -= image_mean
        image = math_ops.divide(image, adjusted_stddev, name=scope)
        return convert_image_dtype(image, orig_dtype, saturate=True)