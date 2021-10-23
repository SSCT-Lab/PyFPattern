def logistic_regression(X, y, class_weight=None, init_mean=None, init_stddev=1.0):
    'Creates logistic regression TensorFlow subgraph.\n\n  Args:\n    X: tensor or placeholder for input features,\n       shape should be [batch_size, n_features].\n    y: tensor or placeholder for target,\n       shape should be [batch_size, n_classes].\n    class_weight: tensor, [n_classes], where for each class\n                  it has weight of the class. If not provided\n                  will check if graph contains tensor `class_weight:0`.\n                  If that is not provided either all ones are used.\n    init_mean: the mean value to use for initialization.\n    init_stddev: the standard devation to use for initialization.\n\n  Returns:\n    Predictions and loss tensors.\n\n  Side effects:\n    The variables linear_regression.weights and linear_regression.bias are\n    initialized as follows.  If init_mean is not None, then initialization\n    will be done using a random normal initializer with the given init_mean\n    and init_stddv.  (These may be set to 0.0 each if a zero initialization\n    is desirable for convex use cases.)  If init_mean is None, then the\n    uniform_unit_scaling_initialzer will be used.\n  '
    with vs.variable_scope('logistic_regression'):
        logging_ops.histogram_summary(('%s.X' % vs.get_variable_scope().name), X)
        logging_ops.histogram_summary(('%s.y' % vs.get_variable_scope().name), y)
        if (init_mean is None):
            weights = vs.get_variable('weights', [X.get_shape()[1], y.get_shape()[(- 1)]])
            bias = vs.get_variable('bias', [y.get_shape()[(- 1)]])
        else:
            weights = vs.get_variable('weights', [X.get_shape()[1], y.get_shape()[(- 1)]], initializer=init_ops.random_normal_initializer(init_mean, init_stddev))
            bias = vs.get_variable('bias', [y.get_shape()[(- 1)]], initializer=init_ops.random_normal_initializer(init_mean, init_stddev))
        logging_ops.histogram_summary(('%s.weights' % vs.get_variable_scope().name), weights)
        logging_ops.histogram_summary(('%s.bias' % vs.get_variable_scope().name), bias)
        if (not class_weight):
            try:
                class_weight = ops.get_default_graph().get_tensor_by_name('class_weight:0')
            except KeyError:
                pass
        return losses_ops.softmax_classifier(X, y, weights, bias, class_weight=class_weight)