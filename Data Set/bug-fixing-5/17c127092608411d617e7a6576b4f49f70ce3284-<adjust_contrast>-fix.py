@tf_export('image.adjust_contrast')
def adjust_contrast(images, contrast_factor):
    'Adjust contrast of RGB or grayscale images.\n\n  This is a convenience method that converts RGB images to float\n  representation, adjusts their contrast, and then converts them back to the\n  original data type. If several adjustments are chained, it is advisable to\n  minimize the number of redundant conversions.\n\n  `images` is a tensor of at least 3 dimensions.  The last 3 dimensions are\n  interpreted as `[height, width, channels]`.  The other dimensions only\n  represent a collection of images, such as `[batch, height, width, channels].`\n\n  Contrast is adjusted independently for each channel of each image.\n\n  For each channel, this Op computes the mean of the image pixels in the\n  channel and then adjusts each component `x` of each pixel to\n  `(x - mean) * contrast_factor + mean`.\n\n  Args:\n    images: Images to adjust.  At least 3-D.\n    contrast_factor: A float multiplier for adjusting contrast.\n\n  Returns:\n    The contrast-adjusted image or images.\n    \n  Usage Example:\n    ```python\n    import tensorflow as tf\n    x = tf.random.normal(shape=(256, 256, 3))\n    tf.image.adjust_contrast(x,2)\n    ```\n  '
    with ops.name_scope(None, 'adjust_contrast', [images, contrast_factor]) as name:
        images = ops.convert_to_tensor(images, name='images')
        orig_dtype = images.dtype
        if (orig_dtype in (dtypes.float16, dtypes.float32)):
            flt_images = images
        else:
            flt_images = convert_image_dtype(images, dtypes.float32)
        adjusted = gen_image_ops.adjust_contrastv2(flt_images, contrast_factor=contrast_factor, name=name)
        return convert_image_dtype(adjusted, orig_dtype, saturate=True)