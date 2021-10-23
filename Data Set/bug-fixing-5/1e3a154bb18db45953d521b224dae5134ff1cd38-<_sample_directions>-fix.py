def _sample_directions(self):
    device = self.device
    xs = self.xs
    params = self.params
    no_gxs = self.no_gxs
    xp = device.xp
    direction_xs_shapes = [x.shape for (x, no_gx) in six.moves.zip(xs, no_gxs) if (not no_gx)]
    direction_param_shapes = [p.shape for p in params]
    direction_shapes = (direction_xs_shapes + direction_param_shapes)
    directions = [xp.random.normal(size=shape) for shape in direction_shapes]
    norm = math.sqrt(sum([xp.square(d).sum() for d in directions]))
    if (norm != 0):
        scale = (1.0 / norm)
        directions = [(d * scale) for d in directions]
    return directions