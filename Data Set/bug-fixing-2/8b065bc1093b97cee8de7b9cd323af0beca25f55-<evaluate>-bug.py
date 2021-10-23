

@abc.abstractmethod
def evaluate(self, x=None, y=None, input_fn=None, feed_fn=None, batch_size=None, steps=None, metrics=None, name=None, checkpoint_path=None, hooks=None):
    'Evaluates given model with provided evaluation data.\n\n    Stop conditions - we evaluate on the given input data until one of the\n    following:\n    - If `steps` is provided, and `steps` batches of size `batch_size` are\n    processed.\n    - If `input_fn` is provided, and it raises an end-of-input\n    exception (`OutOfRangeError` or `StopIteration`).\n    - If `x` is provided, and all items in `x` have been processed.\n\n    The return value is a dict containing the metrics specified in `metrics`, as\n    well as an entry `global_step` which contains the value of the global step\n    for which this evaluation was performed.\n\n    Args:\n      x: Matrix of shape [n_samples, n_features...] or dictionary of many matrices\n         containing the input samples for fitting the model. Can be iterator that returns\n         arrays of features or dictionary of array of features. If set, `input_fn` must\n         be `None`.\n      y: Vector or matrix [n_samples] or [n_samples, n_outputs] containing the\n         label values (class labels in classification, real numbers in\n         regression) or dictionary of multiple vectors/matrices. Can be iterator\n         that returns array of targets or dictionary of array of targets. If set,\n         `input_fn` must be `None`. Note: For classification, label values must\n         be integers representing the class index (i.e. values from 0 to\n         n_classes-1).\n      input_fn: Input function returning a tuple of:\n          features - Dictionary of string feature name to `Tensor` or `Tensor`.\n          labels - `Tensor` or dictionary of `Tensor` with labels.\n        If input_fn is set, `x`, `y`, and `batch_size` must be `None`. If\n        `steps` is not provided, this should raise `OutOfRangeError` or\n        `StopIteration` after the desired amount of data (e.g., one epoch) has\n        been provided. See "Stop conditions" above for specifics.\n      feed_fn: Function creating a feed dict every time it is called. Called\n        once per iteration. Must be `None` if `input_fn` is provided.\n      batch_size: minibatch size to use on the input, defaults to first\n        dimension of `x`, if specified. Must be `None` if `input_fn` is\n        provided.\n      steps: Number of steps for which to evaluate model. If `None`, evaluate\n        until `x` is consumed or `input_fn` raises an end-of-input exception.\n        See "Stop conditions" above for specifics.\n      metrics: Dict of metrics to run. If None, the default metric functions\n        are used; if {}, no metrics are used. Otherwise, `metrics` should map\n        friendly names for the metric to a `MetricSpec` object defining which\n        model outputs to evaluate against which labels with which metric\n        function.\n\n        Metric ops should support streaming, e.g., returning `update_op` and\n        `value` tensors. For example, see the options defined in\n        `../../../metrics/python/ops/metrics_ops.py`.\n      name: Name of the evaluation if user needs to run multiple evaluations on\n        different data sets, such as on training data vs test data.\n      checkpoint_path: Path of a specific checkpoint to evaluate. If `None`, the\n        latest checkpoint in `model_dir` is used.\n      hooks: List of `SessionRunHook` subclass instances. Used for callbacks\n        inside the evaluation call.\n\n    Returns:\n      Returns `dict` with evaluation results.\n    '
    raise NotImplementedError
