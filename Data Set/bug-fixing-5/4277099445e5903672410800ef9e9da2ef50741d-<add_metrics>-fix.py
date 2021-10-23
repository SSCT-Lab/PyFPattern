def add_metrics(estimator, metric_fn):
    "Creates new ${tf.estimator.Estimator} which has given metrics.\n\n  Example:\n\n  ```python\n    def my_auc(labels, predictions):\n      return {'auc': tf.metrics.auc(labels, predictions['logistic'])}\n\n    estimator = tf.estimator.DNNClassifier(...)\n    estimator = tf.contrib.estimator.add_metrics(estimator, my_auc)\n    estimator.train(...)\n    estimator.evaluate(...)\n  ```\n  Example usage of custom metric which uses features:\n\n  ```python\n    def my_auc(features, labels, predictions):\n      return {'auc': tf.metrics.auc(\n        labels, predictions['logistic'], weights=features['weight'])}\n\n    estimator = tf.estimator.DNNClassifier(...)\n    estimator = tf.contrib.estimator.add_metrics(estimator, my_auc)\n    estimator.train(...)\n    estimator.evaluate(...)\n  ```\n\n  Args:\n    estimator: A ${tf.estimator.Estimator} object.\n    metric_fn: A function which should obey the following signature:\n      - Args: can only have following four arguments in any order:\n        * predictions: Predictions `Tensor` or dict of `Tensor` created by given\n          `estimator`.\n        * features: Input `dict` of `Tensor` objects created by `input_fn` which\n          is given to `estimator.evaluate` as an argument.\n        * labels:  Labels `Tensor` or dict of `Tensor` created by `input_fn`\n          which is given to `estimator.evaluate` as an argument.\n        * config: config attribute of the `estimator`.\n       - Returns:\n         Dict of metric results keyed by name. Final metrics are a union of this\n         and `estimator's` existing metrics. If there is a name conflict between\n         this and `estimator`s existing metrics, this will override the existing\n         one. The values of the dict are the results of calling a metric\n         function, namely a `(metric_tensor, update_op)` tuple.\n\n  Returns:\n      A new ${tf.estimator.Estimator} which has a union of original metrics with\n        given ones.\n  "
    _verify_metric_fn_args(metric_fn)

    def new_model_fn(features, labels, mode):
        spec = _get_model_fn(estimator)(features, labels, mode)
        if (mode != model_fn_lib.ModeKeys.EVAL):
            return spec
        new_metrics = _call_metric_fn(metric_fn, features, labels, spec.predictions, estimator.config)
        all_metrics = (spec.eval_metric_ops or {
            
        })
        all_metrics.update(new_metrics)
        return spec._replace(eval_metric_ops=all_metrics)
    return estimator_lib.Estimator(model_fn=new_model_fn, model_dir=estimator.model_dir, config=estimator.config)