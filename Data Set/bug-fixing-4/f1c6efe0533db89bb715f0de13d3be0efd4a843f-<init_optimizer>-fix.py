def init_optimizer(self, kvstore='local', optimizer='sgd', optimizer_params=(('learning_rate', 0.01),), force_init=False):
    "Install and initialize optimizers.\n\n        Parameters\n        ----------\n        kvstore : str or KVStore\n            Default `'local'`.\n        optimizer : str or Optimizer\n            Default `'sgd'`\n        optimizer_params : dict\n            Default `(('learning_rate', 0.01),)`. The default value is not a dictionary,\n            just to avoid pylint warning of dangerous default values.\n        force_init : bool\n            Default `False`, indicating whether we should force re-initializing the\n            optimizer in the case an optimizer is already installed.\n        "
    assert (self.binded and self.params_initialized)
    if (self.optimizer_initialized and (not force_init)):
        self.logger.warning('optimizer already initialized, ignoring.')
        return
    self._curr_module.init_optimizer(kvstore, optimizer, optimizer_params, force_init=force_init)
    for mod in self._buckets.values():
        if (mod is not self._curr_module):
            mod.borrow_optimizer(self._curr_module)
    self.optimizer_initialized = True