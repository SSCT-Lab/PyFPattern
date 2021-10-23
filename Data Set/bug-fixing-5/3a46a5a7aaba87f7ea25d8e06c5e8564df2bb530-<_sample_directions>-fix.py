def _sample_directions(self):
    device = self.device
    xs = self.xs
    params = self.params
    no_gxs = self.no_gxs
    xp = device.xp
    direction_xs_shapes = [(None if (x is None) else x.shape) for (x, no_gx) in six.moves.zip(xs, no_gxs) if (not no_gx)]
    direction_param_shapes = [p.shape for p in params]
    direction_shapes = (direction_xs_shapes + direction_param_shapes)
    directions = [(None if (shape is None) else xp.random.normal(size=shape)) for shape in direction_shapes]
    if all([((d is None) or (d.size == 0)) for d in directions]):
        return directions
    none_indices = [i for (i, d) in enumerate(directions) if (d is None)]
    directions = [d for d in directions if (d is not None)]
    norm = math.sqrt(sum([xp.square(d).sum() for d in directions]))
    scale = (1.0 / norm)
    directions = [xp.asarray((d * scale)) for d in directions]
    min_d = (0.1 / math.sqrt(sum([d.size for d in directions])))
    is_small = [(min_d > xp.abs(d)) for d in directions]
    is_large = [xp.logical_not(iss) for iss in is_small]
    n_small = sum([iss.sum() for iss in is_small])
    sq_large = sum([xp.square(d[isl]).sum() for (d, isl) in zip(directions, is_large)])
    scale = xp.sqrt(((1 - (n_small * (min_d ** 2))) / sq_large))
    for (d, iss, isl) in zip(directions, is_small, is_large):
        d[iss] = (xp.sign(d[iss]) * min_d)
        d[isl] *= scale
    for i in none_indices:
        directions.insert(i, None)
    return directions