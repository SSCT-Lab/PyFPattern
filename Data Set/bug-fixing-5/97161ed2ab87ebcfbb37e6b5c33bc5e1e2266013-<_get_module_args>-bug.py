def _get_module_args(self, fact_module, task_vars):
    mod_args = self._task.args.copy()
    if (fact_module != 'setup'):
        if (self._connection._load_name not in ('network_cli', 'httpapi', 'netconf')):
            subset = mod_args.pop('gather_subset', None)
            if (subset not in ('all', ['all'])):
                self._display.warning(('Ignoring subset(%s) for %s' % (subset, fact_module)))
        timeout = mod_args.pop('gather_timeout', None)
        if (timeout is not None):
            self._display.warning(('Ignoring timeout(%s) for %s' % (timeout, fact_module)))
        fact_filter = mod_args.pop('filter', None)
        if (fact_filter is not None):
            self._display.warning(('Ignoring filter(%s) for %s' % (fact_filter, fact_module)))
    return mod_args