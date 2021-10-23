def __init__(self, name='weight', n_power_iterations=1, eps=1e-12):
    self.name = name
    if (n_power_iterations <= 0):
        raise ValueError('Expected n_power_iterations to be positive, but got n_power_iterations={}'.format(n_power_iterations))
    self.n_power_iterations = n_power_iterations
    self.eps = eps