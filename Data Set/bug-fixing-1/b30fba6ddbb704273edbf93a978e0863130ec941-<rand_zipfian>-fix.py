

def rand_zipfian(true_classes, num_sampled, range_max):
    "Draw random samples from an approximately log-uniform or Zipfian distribution.\n\n    This operation randomly samples *num_sampled* candidates the range of integers [0, range_max).\n    The elements of sampled_candidates are drawn with replacement from the base distribution.\n\n    The base distribution for this operator is an approximately log-uniform or Zipfian distribution:\n\n    P(class) = (log(class + 2) - log(class + 1)) / log(range_max + 1)\n\n    This sampler is useful when the true classes approximately follow such a distribution.\n    For example, if the classes represent words in a lexicon sorted in decreasing order of     frequency. If your classes are not ordered by decreasing frequency, do not use this op.\n\n    Additionaly, it also returns the number of times each of the     true classes and the sampled classes is expected to occur.\n\n    Parameters\n    ----------\n    true_classes : Symbol\n        The target classes in 1-D.\n    num_sampled: int\n        The number of classes to randomly sample.\n    range_max: int\n        The number of possible classes.\n\n    Returns\n    -------\n    samples: Symbol\n        The sampled candidate classes in 1-D `int64` dtype.\n    expected_count_true: Symbol\n        The expected count for true classes in 1-D `float64` dtype.\n    expected_count_sample: Symbol\n        The expected count for sampled candidates in 1-D `float64` dtype.\n\n    Examples\n    --------\n    >>> true_cls = mx.sym.Variable('true_cls')\n    >>> samples, exp_count_true, exp_count_sample = mx.sym.contrib.rand_zipfian(true_cls, 4, 5)\n    >>> samples.eval(true_cls=mx.nd.array([3]))[0].asnumpy()\n    array([1, 3, 3, 3])\n    >>> exp_count_true.eval(true_cls=mx.nd.array([3]))[0].asnumpy()\n    array([0.12453879])\n    >>> exp_count_sample.eval(true_cls=mx.nd.array([3]))[0].asnumpy()\n    array([0.22629439, 0.12453879, 0.12453879, 0.12453879])\n    "
    assert isinstance(true_classes, Symbol), ('unexpected type %s' % type(true_classes))
    log_range = math.log((range_max + 1))
    rand = uniform(0, log_range, shape=(num_sampled,), dtype='float64')
    sampled_classes = ((rand.exp() - 1).astype('int64') % range_max)
    true_classes = true_classes.astype('float64')
    expected_prob_true = (((true_classes + 2.0) / (true_classes + 1.0)).log() / log_range)
    expected_count_true = (expected_prob_true * num_sampled)
    sampled_cls_fp64 = sampled_classes.astype('float64')
    expected_prob_sampled = (((sampled_cls_fp64 + 2.0) / (sampled_cls_fp64 + 1.0)).log() / log_range)
    expected_count_sampled = (expected_prob_sampled * num_sampled)
    return (sampled_classes, expected_count_true, expected_count_sampled)
