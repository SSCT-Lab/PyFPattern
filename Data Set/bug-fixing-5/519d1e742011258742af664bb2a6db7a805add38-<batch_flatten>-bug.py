def batch_flatten(x):
    'Turn a n-D tensor into a 2D tensor where\n    the first dimension is conserved.\n    '
    x = tf.reshape(x, [(- 1), prod(shape(x)[1:])])
    return x