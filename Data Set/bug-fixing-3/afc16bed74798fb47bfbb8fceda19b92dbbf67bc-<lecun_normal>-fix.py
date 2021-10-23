@tf_export('keras.initializers.lecun_normal')
def lecun_normal(seed=None):
    'LeCun normal initializer.\n\n  It draws samples from a truncated normal distribution centered on 0\n  with `stddev = sqrt(1 / fan_in)`\n  where `fan_in` is the number of input units in the weight tensor.\n\n  Arguments:\n      seed: A Python integer. Used to seed the random generator.\n\n  Returns:\n      An initializer.\n\n  References:\n      - [Self-Normalizing Neural Networks](https://arxiv.org/abs/1706.02515)\n      - [Efficient\n      Backprop](http://yann.lecun.com/exdb/publis/pdf/lecun-98b.pdf)\n  '
    return VarianceScaling(scale=1.0, mode='fan_in', distribution='truncated_normal', seed=seed)