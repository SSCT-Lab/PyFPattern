def v2_runner_item_on_failed(self, result):
    delegated_vars = result._result.get('_ansible_delegated_vars', None)
    self._clean_results(result._result, result._task.action)
    self._handle_exception(result._result)
    msg = 'failed: '
    if delegated_vars:
        msg += ('[%s -> %s]' % (result._host.get_name(), delegated_vars['ansible_host']))
    else:
        msg += ('[%s]' % result._host.get_name())
    self._handle_warnings(result._result)
    self._display.display((msg + (' (item=%s) => %s' % (self._get_item_label(result._result), self._dump_results(result._result)))), color=C.COLOR_ERROR)