def _clean_results(self, result, task_name):
    ' removes data from results for display '
    if (task_name in ['debug']):
        for hideme in self._hide_in_debug:
            result.pop(hideme, None)