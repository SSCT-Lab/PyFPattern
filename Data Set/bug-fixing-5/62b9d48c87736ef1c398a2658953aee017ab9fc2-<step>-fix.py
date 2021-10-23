def step(self, batch_size, ignore_stale_grad=False):
    'Makes one step of parameter update. Should be called after\n        `autograd.compute_gradient` and outside of `record()` scope.\n\n        Parameters\n        ----------\n        batch_size : int\n            Batch size of data processed. Gradient will be normalized by `1/batch_size`.\n            Set this to 1 if you normalized loss manually with `loss = mean(loss)`.\n        ignore_stale_grad : bool, optional, default=False\n            If true, ignores Parameters with stale gradient (gradient that has not\n            been updated by `backward` after last step) and skip update.\n        '
    if (not self._kv_initialized):
        self._init_kvstore()
    self._optimizer.rescale_grad = (self._scale / batch_size)
    for (i, param) in enumerate(self._params):
        if (param.grad_req == 'null'):
            continue
        if (not ignore_stale_grad):
            for data in param.list_data():
                if (not data._fresh_grad):
                    raise UserWarning(('Gradient of Parameter `%s` on context %s has not been updated by backward since last `step`. This could mean a bug in your model that made it only use a subset of the Parameters (Blocks) for this iteration. If you are intentionally only using a subset, call step with ignore_stale_grad=True to suppress this warning and skip updating of Parameters with stale gradient' % (param.name, str(data.context))))
        if self._kvstore:
            self._kvstore.push(i, param.list_grad(), priority=(- i))
            if self._update_on_kvstore:
                self._kvstore.pull(i, param.list_data(), priority=(- i))
                continue
            else:
                self._kvstore.pull(i, param.list_grad(), priority=(- i))
        for (upd, arr, grad) in zip(self._updaters, param.list_data(), param.list_grad()):
            if ((not ignore_stale_grad) or arr._fresh_grad):
                upd(i, grad, arr)
                arr._fresh_grad = False