

def load_states(self, fname):
    'Loads trainer states (e.g. optimizer, momentum) from a file.\n\n        Parameters\n        ----------\n        fname : str\n            Path to input states file.\n        '
    if (not self._kv_initialized):
        self._init_kvstore()
    if self._update_on_kvstore:
        self._kvstore.load_optimizer_states(fname)
        self._optimizer = self._kvstore._updater.optimizer
    else:
        with open(fname, 'rb') as f:
            states = f.read()
        for updater in self._updaters:
            updater.set_states(states)
            updater.optimizer = self._updaters[0].optimizer
        self._optimizer = self._updaters[0].optimizer
