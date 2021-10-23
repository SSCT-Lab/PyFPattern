

def elu(x, alpha=1.0):
    'Exponential linear unit.\n\n    # Arguments\n        x: A tensor or variable to compute the activation function for.\n        alpha: A scalar, slope of positive section.\n\n    # Returns\n        A tensor.\n    '
    res = tf.nn.elu(x)
    if (alpha == 1):
        return res
    else:
        return tf.where((x > 0), res, (alpha * res))
