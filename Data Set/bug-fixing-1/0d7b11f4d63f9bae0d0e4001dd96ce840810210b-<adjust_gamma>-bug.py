

@tf_export('image.adjust_gamma')
def adjust_gamma(image, gamma=1, gain=1):
    'Performs Gamma Correction on the input image.\n\n  Also known as Power Law Transform. This function transforms the\n  input image pixelwise according to the equation `Out = In**gamma`\n  after scaling each pixel to the range 0 to 1.\n\n  Args:\n    image : A Tensor.\n    gamma : A scalar or tensor. Non negative real number.\n    gain  : A scalar or tensor. The constant multiplier.\n\n  Returns:\n    A Tensor. Gamma corrected output image.\n\n  Raises:\n    ValueError: If gamma is negative.\n\n  Notes:\n    For gamma greater than 1, the histogram will shift towards left and\n    the output image will be darker than the input image.\n    For gamma less than 1, the histogram will shift towards right and\n    the output image will be brighter than the input image.\n\n  References:\n    [1] http://en.wikipedia.org/wiki/Gamma_correction\n  '
    with ops.op_scope([image, gamma, gain], None, 'adjust_gamma'):
        img = ops.convert_to_tensor(image, name='img', dtype=dtypes.float32)
        image = ops.convert_to_tensor(image, name='image')
        assert_op = _assert((gamma >= 0), ValueError, 'Gamma should be a non-negative real number.')
        if assert_op:
            gamma = control_flow_ops.with_dependencies(assert_op, gamma)
        scale = constant_op.constant((image.dtype.limits[1] - image.dtype.limits[0]), dtype=dtypes.float32)
        adjusted_img = ((((img / scale) ** gamma) * scale) * gain)
        return adjusted_img
