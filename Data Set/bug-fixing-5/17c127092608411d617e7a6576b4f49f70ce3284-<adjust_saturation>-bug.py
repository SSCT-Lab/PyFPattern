@tf_export('image.adjust_saturation')
def adjust_saturation(image, saturation_factor, name=None):
    'Adjust saturation of RGB images.\n\n  This is a convenience method that converts RGB images to float\n  representation, converts them to HSV, add an offset to the saturation channel,\n  converts back to RGB and then back to the original data type. If several\n  adjustments are chained it is advisable to minimize the number of redundant\n  conversions.\n\n  `image` is an RGB image or images.  The image saturation is adjusted by\n  converting the images to HSV and multiplying the saturation (S) channel by\n  `saturation_factor` and clipping. The images are then converted back to RGB.\n\n  Args:\n    image: RGB image or images. Size of the last dimension must be 3.\n    saturation_factor: float. Factor to multiply the saturation by.\n    name: A name for this operation (optional).\n\n  Returns:\n    Adjusted image(s), same shape and DType as `image`.\n\n  Usage Example:\n    ```python\n    >> import tensorflow as tf\n    >> x = tf.random.normal(shape=(256, 256, 3))\n    >> tf.image.adjust_saturation(x, 0.5)\n    ```\n\n  Raises:\n    InvalidArgumentError: input must have 3 channels\n  '
    with ops.name_scope(name, 'adjust_saturation', [image]) as name:
        image = ops.convert_to_tensor(image, name='image')
        orig_dtype = image.dtype
        if (orig_dtype in (dtypes.float16, dtypes.float32)):
            flt_image = image
        else:
            flt_image = convert_image_dtype(image, dtypes.float32)
        adjusted = gen_image_ops.adjust_saturation(flt_image, saturation_factor)
        return convert_image_dtype(adjusted, orig_dtype)