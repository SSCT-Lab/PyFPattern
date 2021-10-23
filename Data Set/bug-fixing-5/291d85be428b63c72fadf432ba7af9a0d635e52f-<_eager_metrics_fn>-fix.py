def _eager_metrics_fn(model, outputs, targets):
    'Calculates the metrics for each output of the given model.\n\n  Arguments:\n      model: The model on which metrics are being calculated.\n      outputs: The outputs of the given model.\n      targets: The predictions or targets of the given model.\n\n  Returns:\n      Returns the metric names and metric results for each output of the model.\n  '
    metric_names = []
    metric_results = []
    if (not isinstance(outputs, list)):
        outputs = [outputs]
    if (not isinstance(targets, list)):
        targets = [targets]
    for i in range(len(model.outputs)):
        output_metrics = model.nested_metrics[i]
        for nested_output_metric in output_metrics:
            (metric_name, metric_fn) = _get_metrics_info(nested_output_metric, backend.int_shape(model.outputs[i]), model.loss_functions[i])
            if (len(model.output_names) > 1):
                metric_name = ((model.output_names[i] + '_') + metric_name)
                if (metric_name not in model.metrics_names):
                    model.metrics_names.append(metric_name)
            with backend.name_scope(metric_name):
                metric_result = metric_fn(targets[i], outputs[i])
                metric_names.append(metric_name)
                metric_results.append(backend.mean(metric_result))
    return metric_results