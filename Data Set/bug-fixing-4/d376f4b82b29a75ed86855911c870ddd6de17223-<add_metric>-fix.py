def add_metric(self, metric):
    '\n        Add a new metric to container. Noted that the argument list \n        of the added one should be consistent with existed ones.  \n\n        Args:\n            metric(MetricBase): a instance of MetricBase\n        '
    if (not isinstance(metric, MetricBase)):
        raise ValueError('SubMetric should be inherit from MetricBase.')
    self._metrics.append(metric)