

def _interpolate(name, dim, interpolate_mode):

    def symbolic_fn(g, input, output_size, align_corners=None):
        align_corners = sym_help._maybe_get_scalar(align_corners)
        output_size = sym_help._maybe_get_const(output_size, 'is')
        if sym_help._is_value(output_size):
            offsets = g.op('Constant', value_t=torch.ones(offset, dtype=torch.int64))
            output_size = g.op('Concat', offsets, output_size, axis_i=0)
        else:
            output_size = [(1 if (i < 2) else output_size[(- (dim - i))]) for i in range(0, dim)]
            output_size = g.op('Constant', value_t=torch.tensor(output_size))
        coordinate_transformation_mode = ('asymmetric' if (interpolate_mode == 'nearest') else ('align_corners' if align_corners else 'pytorch_half_pixel'))
        empty_tensor = g.op('Constant', value_t=torch.tensor([], dtype=torch.float32))
        return g.op('Resize', input, empty_tensor, empty_tensor, output_size, coordinate_transformation_mode_s=coordinate_transformation_mode, cubic_coeff_a_f=(- 0.75), mode_s=interpolate_mode, nearest_mode_s='floor')
    return symbolic_fn
