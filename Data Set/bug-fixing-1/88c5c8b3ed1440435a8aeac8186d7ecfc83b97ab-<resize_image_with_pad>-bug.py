

@tf_export('image.resize_image_with_pad')
def resize_image_with_pad(image, target_height, target_width, method=ResizeMethod.BILINEAR):
    "Resizes and pads an image to a target width and height.\n\n  Resizes an image to a target width and height by keeping\n  the aspect ratio the same without distortion. If the target\n  dimensions don't match the image dimensions, the image\n  is resized and then padded with zeroes to match requested\n  dimensions.\n\n  Args:\n    image: 4-D Tensor of shape `[batch, height, width, channels]` or\n           3-D Tensor of shape `[height, width, channels]`.\n    target_height: Target height.\n    target_width: Target width.\n    method: Method to use for resizing image. See `resize_images()`\n\n  Raises:\n    ValueError: if `target_height` or `target_width` are zero or negative.\n\n  Returns:\n    Resized and padded image.\n    If `images` was 4-D, a 4-D float Tensor of shape\n    `[batch, new_height, new_width, channels]`.\n    If `images` was 3-D, a 3-D float Tensor of shape\n    `[new_height, new_width, channels]`.\n  "
    with ops.name_scope(None, 'resize_image_with_pad', [image]):
        image = ops.convert_to_tensor(image, name='image')
        image_shape = image.get_shape()
        is_batch = True
        if (image_shape.ndims == 3):
            is_batch = False
            image = array_ops.expand_dims(image, 0)
        elif (image_shape.ndims is None):
            is_batch = False
            image = array_ops.expand_dims(image, 0)
            image.set_shape(([None] * 4))
        elif (image_shape.ndims != 4):
            raise ValueError("'image' must have either 3 or 4 dimensions.")
        assert_ops = _CheckAtLeast3DImage(image, require_static=False)
        assert_ops += _assert((target_width > 0), ValueError, 'target_width must be > 0.')
        assert_ops += _assert((target_height > 0), ValueError, 'target_height must be > 0.')
        image = control_flow_ops.with_dependencies(assert_ops, image)

        def max_(x, y):
            if (_is_tensor(x) or _is_tensor(y)):
                return math_ops.maximum(x, y)
            else:
                return max(x, y)
        (_, height, width, _) = _ImageDimensions(image, rank=4)
        f_height = math_ops.cast(height, dtype=dtypes.float64)
        f_width = math_ops.cast(width, dtype=dtypes.float64)
        f_target_height = math_ops.cast(target_height, dtype=dtypes.float64)
        f_target_width = math_ops.cast(target_width, dtype=dtypes.float64)
        ratio = max_((f_width / f_target_width), (f_height / f_target_height))
        resized_height_float = (f_height / ratio)
        resized_width_float = (f_width / ratio)
        resized_height = math_ops.cast(math_ops.floor(resized_height_float), dtype=dtypes.int32)
        resized_width = math_ops.cast(math_ops.floor(resized_width_float), dtype=dtypes.int32)
        padding_height = ((f_target_height - resized_height_float) / 2)
        padding_width = ((f_target_width - resized_width_float) / 2)
        f_padding_height = math_ops.floor(padding_height)
        f_padding_width = math_ops.floor(padding_width)
        p_height = max_(0, math_ops.cast(f_padding_height, dtype=dtypes.int32))
        p_width = max_(0, math_ops.cast(f_padding_width, dtype=dtypes.int32))
        resized = resize_images(image, [resized_height, resized_width], method)
        padded = pad_to_bounding_box(resized, p_height, p_width, target_height, target_width)
        if (padded.get_shape().ndims is None):
            raise ValueError('padded contains no shape.')
        _ImageDimensions(padded, rank=4)
        if (not is_batch):
            padded = array_ops.squeeze(padded, squeeze_dims=[0])
        return padded
