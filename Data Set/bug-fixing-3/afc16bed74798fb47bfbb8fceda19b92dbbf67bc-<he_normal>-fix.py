@tf_export('keras.initializers.he_normal')
def he_normal(seed=None):
    'He normal initializer.\n\n  It draws samples from a truncated normal distribution centered on 0\n  with `stddev = sqrt(2 / fan_in)`\n  where `fan_in` is the number of input units in the weight tensor.\n\n  Arguments:\n      seed: A Python integer. Used to seed the random generator.\n\n  Returns:\n      An initializer.\n\n  References:\n      He et al., http://arxiv.org/abs/1502.01852\n  '
    return VarianceScaling(scale=2.0, mode='fan_in', distribution='truncated_normal', seed=seed)