def _call_batch_hook(self, mode, hook, batch, logs=None):
    'Helper function for all batch_{begin | end} methods.'
    if (not self.callbacks):
        return
    hook_name = 'on_{mode}_batch_{hook}'.format(mode=mode, hook=hook)
    if (hook == 'end'):
        if (not hasattr(self, '_t_enter_batch')):
            self._t_enter_batch = time.time()
        self._delta_t_batch = (time.time() - self._t_enter_batch)
    logs = (logs or {
        
    })
    t_before_callbacks = time.time()
    for callback in self.callbacks:
        batch_hook = getattr(callback, hook_name)
        batch_hook(batch, logs)
    self._delta_ts[hook_name].append((time.time() - t_before_callbacks))
    delta_t_median = np.median(self._delta_ts[hook_name])
    if ((self._delta_t_batch > 0.0) and (delta_t_median > (0.95 * self._delta_t_batch)) and (delta_t_median > 0.1)):
        warnings.warn(('Method (%s) is slow compared to the batch update (%f). Check your callbacks.' % (hook_name, delta_t_median)), RuntimeWarning)
    if (hook == 'begin'):
        self._t_enter_batch = time.time()