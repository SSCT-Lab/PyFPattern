

def flip_up_down(image):
    'Flip an image horizontally (upside down).\n\n  Outputs the contents of `image` flipped along the first dimension, which is\n  `height`.\n\n  See also `reverse()`.\n\n  Args:\n    image: A 3-D tensor of shape `[height, width, channels].`\n\n  Returns:\n    A 3-D tensor of the same type and shape as `image`.\n\n  Raises:\n    ValueError: if the shape of `image` not supported.\n  '
    image = ops.convert_to_tensor(image, name='image')
    image = control_flow_ops.with_dependencies(_Check3DImage(image, require_static=False), image)
    return fix_image_flip_shape(image, array_ops.reverse(image, [0]))
