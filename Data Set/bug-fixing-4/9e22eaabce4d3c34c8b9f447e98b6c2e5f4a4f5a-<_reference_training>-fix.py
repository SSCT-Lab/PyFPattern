def _reference_training(self, x, scale, offset, epsilon, data_format):
    if (data_format != 'NHWC'):
        raise ValueError(('data_format must be NHWC, got %s.' % data_format))
    x_square = (x * x)
    x_square_sum = np.sum(x_square, (0, 1, 2))
    x_sum = np.sum(x, axis=(0, 1, 2))
    element_count = (np.size(x) / int(np.shape(x)[(- 1)]))
    mean = (x_sum / element_count)
    var = ((x_square_sum / element_count) - (mean * mean))
    normalized = ((x - mean) / np.sqrt((var + epsilon)))
    return (((normalized * scale) + offset), mean, var)