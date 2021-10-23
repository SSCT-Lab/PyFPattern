def _sample_directions(self):
    device = self.device
    x_data = self.x_data
    params = self.params
    no_grads = self.no_grads
    xp = device.xp
    direction_xs_shapes = [x.shape for (x, no_grad) in six.moves.zip(x_data, no_grads) if (not no_grad)]
    direction_param_shapes = [p.shape for p in params]
    direction_shapes = (direction_xs_shapes + direction_param_shapes)
    directions = [xp.random.normal(size=shape) for shape in direction_shapes]
    norm = math.sqrt(sum([xp.square(d).sum() for d in directions]))
    if (norm != 0):
        scale = (1.0 / norm)
        directions = [(d * scale) for d in directions]
    return directions