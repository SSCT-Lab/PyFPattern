def clean_copy(self):
    " returns 'clean' taskresult object "
    result = TaskResult(self._host, self._task, {
        
    }, self._task_fields)
    if (result._task and (result._task.action in ['debug'])):
        ignore = (_IGNORE + ('invocation',))
    else:
        ignore = _IGNORE
    if self._result.get('_ansible_no_log', False):
        result._result = {
            'censored': "the output has been hidden due to the fact that 'no_log: true' was specified for this result",
        }
    elif self._result:
        result._result = deepcopy(self._result)
        for remove_key in ignore:
            if (remove_key in result._result):
                del result._result[remove_key]
        strip_internal_keys(result._result, exceptions=('_ansible_verbose_always', '_ansible_item_label', '_ansible_no_log'))
    return result