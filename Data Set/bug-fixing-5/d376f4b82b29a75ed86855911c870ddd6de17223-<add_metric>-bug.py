def add_metric(self, metric):
    '\n        add one metric instance to CompositeMetric.\n\n        Args:\n            metric: a instance of MetricBase.\n        '
    if (not isinstance(metric, MetricBase)):
        raise ValueError('SubMetric should be inherit from MetricBase.')
    self._metrics.append(metric)