@tf_export('image.adjust_brightness')
def adjust_brightness(image, delta):
    'Adjust the brightness of RGB or Grayscale images.\n\n  This is a convenience method that converts RGB images to float\n  representation, adjusts their brightness, and then converts them back to the\n  original data type. If several adjustments are chained, it is advisable to\n  minimize the number of redundant conversions.\n\n  The value `delta` is added to all components of the tensor `image`. `image` is\n  converted to `float` and scaled appropriately if it is in fixed-point\n  representation, and `delta` is converted to the same data type. For regular\n  images, `delta` should be in the range `[0,1)`, as it is added to the image in\n  floating point representation, where pixel values are in the `[0,1)` range.\n\n  Args:\n    image: RGB image or images to adjust.\n    delta: A scalar. Amount to add to the pixel values.\n\n  Returns:\n    A brightness-adjusted tensor of the same shape and type as `image`.\n\n  Usage Example:\n    ```python\n    import tensorflow as tf\n    x = tf.random.normal(shape=(256, 256, 3))\n    tf.image.adjust_brightness(x, delta=0.1)\n    ```\n  '
    with ops.name_scope(None, 'adjust_brightness', [image, delta]) as name:
        image = ops.convert_to_tensor(image, name='image')
        orig_dtype = image.dtype
        if (orig_dtype in [dtypes.float16, dtypes.float32]):
            flt_image = image
        else:
            flt_image = convert_image_dtype(image, dtypes.float32)
        adjusted = math_ops.add(flt_image, math_ops.cast(delta, flt_image.dtype), name=name)
        return convert_image_dtype(adjusted, orig_dtype, saturate=True)