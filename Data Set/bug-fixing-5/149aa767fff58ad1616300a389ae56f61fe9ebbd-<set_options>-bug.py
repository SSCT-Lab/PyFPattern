def set_options(self, task_keys=None, var_options=None, direct=None):
    super(NetworkConnectionBase, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)
    self._cached_variables = (task_keys, var_options, direct)