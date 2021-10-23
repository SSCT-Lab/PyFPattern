@tf_export('image.convert_image_dtype')
def convert_image_dtype(image, dtype, saturate=False, name=None):
    "Convert `image` to `dtype`, scaling its values if needed.\n\n  Images that are represented using floating point values are expected to have\n  values in the range [0,1). Image data stored in integer data types are\n  expected to have values in the range `[0,MAX]`, where `MAX` is the largest\n  positive representable number for the data type.\n\n  This op converts between data types, scaling the values appropriately before\n  casting.\n\n  Note that converting from floating point inputs to integer types may lead to\n  over/underflow problems. Set saturate to `True` to avoid such problem in\n  problematic conversions. If enabled, saturation will clip the output into the\n  allowed range before performing a potentially dangerous cast (and only before\n  performing such a cast, i.e., when casting from a floating point to an integer\n  type, and when casting from a signed to an unsigned type; `saturate` has no\n  effect on casts between floats, or on casts that increase the type's range).\n\n  Args:\n    image: An image.\n    dtype: A `DType` to convert `image` to.\n    saturate: If `True`, clip the input before casting (if necessary).\n    name: A name for this operation (optional).\n\n  Returns:\n    `image`, converted to `dtype`.\n\n  Usage Example:\n    ```python\n    >> import tensorflow as tf\n    >> x = tf.random.normal(shape=(256, 256, 3), dtype=tf.float32)\n    >> tf.image.convert_image_dtype(x, dtype=tf.float16, saturate=False)\n    ```\n\n  Raises:\n    AttributeError: Raises an attribute error when dtype is neither\n    float nor integer\n  "
    image = ops.convert_to_tensor(image, name='image')
    dtype = dtypes.as_dtype(dtype)
    if ((not dtype.is_floating) and (not dtype.is_integer)):
        raise AttributeError('dtype must be either floating point or integer')
    if (dtype == image.dtype):
        return array_ops.identity(image, name=name)
    with ops.name_scope(name, 'convert_image', [image]) as name:
        if (image.dtype.is_integer and dtype.is_integer):
            scale_in = image.dtype.max
            scale_out = dtype.max
            if (scale_in > scale_out):
                scale = ((scale_in + 1) // (scale_out + 1))
                scaled = math_ops.div(image, scale)
                if saturate:
                    return math_ops.saturate_cast(scaled, dtype, name=name)
                else:
                    return math_ops.cast(scaled, dtype, name=name)
            else:
                if saturate:
                    cast = math_ops.saturate_cast(image, dtype)
                else:
                    cast = math_ops.cast(image, dtype)
                scale = ((scale_out + 1) // (scale_in + 1))
                return math_ops.multiply(cast, scale, name=name)
        elif (image.dtype.is_floating and dtype.is_floating):
            return math_ops.cast(image, dtype, name=name)
        elif image.dtype.is_integer:
            cast = math_ops.cast(image, dtype)
            scale = (1.0 / image.dtype.max)
            return math_ops.multiply(cast, scale, name=name)
        else:
            scale = (dtype.max + 0.5)
            scaled = math_ops.multiply(image, scale)
            if saturate:
                return math_ops.saturate_cast(scaled, dtype, name=name)
            else:
                return math_ops.cast(scaled, dtype, name=name)