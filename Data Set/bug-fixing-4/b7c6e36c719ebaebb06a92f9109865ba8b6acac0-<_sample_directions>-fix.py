def _sample_directions(self):
    device = self.device
    xs = self.xs
    params = self.params
    no_gxs = self.no_gxs
    xp = device.xp
    direction_xs_shapes = [(None if (x is None) else x.shape) for (x, no_gx) in six.moves.zip(xs, no_gxs) if (not no_gx)]
    direction_param_shapes = [p.shape for p in params]
    direction_shapes = (direction_xs_shapes + direction_param_shapes)
    total_size = sum([int(numpy.prod(shape)) for shape in direction_shapes if (shape is not None)])
    directions = xp.random.normal(size=(total_size,))
    if (total_size > 0):
        directions /= xp.sqrt(xp.square(directions).sum())
        min_d = (0.1 / math.sqrt(total_size))
        is_small = (min_d > xp.abs(directions))
        is_large = xp.logical_not(is_small)
        n_small = is_small.sum()
        sq_large = xp.square(directions[is_large]).sum()
        scale = xp.sqrt(((1 - (n_small * (min_d ** 2))) / sq_large))
        directions[is_small] = (xp.sign(directions[is_small]) * min_d)
        directions[is_large] *= scale
    return self._unpack_arrays(xp, directions, direction_shapes)