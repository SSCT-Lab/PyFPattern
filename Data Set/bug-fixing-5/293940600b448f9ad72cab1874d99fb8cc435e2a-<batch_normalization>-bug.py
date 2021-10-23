def batch_normalization(x, mean, var, beta, gamma, epsilon=0.001):
    'Applies batch normalization on x given mean, var, beta and gamma:\n\n    output = (x - mean) / (sqrt(var) + epsilon) * gamma + beta\n    '
    return tf.nn.batch_normalization(x, mean, var, beta, gamma, epsilon)