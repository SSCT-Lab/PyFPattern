def update_metric(self, eval_metric, labels):
    'Evaluate and accumulate evaluation metric on outputs of the last forward computation.\n\n        Parameters\n        ----------\n        eval_metric : EvalMetric\n        labels : list of NDArray\n            Typically `data_batch.label`.\n        '
    assert (self.binded and self.params_initialized)
    for (meta, module) in zip(self._metas, self._modules):
        if (meta.has_key(SequentialModule.META_TAKE_LABELS) and meta[SequentialModule.META_TAKE_LABELS]):
            module.update_metric(eval_metric, labels)