def v2_runner_item_on_ok(self, result):
    if (not self._plugin_options.get('display_ok_hosts', DEFAULT_DISPLAY_OK_HOSTS)):
        return
    delegated_vars = result._result.get('_ansible_delegated_vars', None)
    self._clean_results(result._result, result._task.action)
    if isinstance(result._task, TaskInclude):
        return
    elif result._result.get('changed', False):
        msg = 'changed'
        color = C.COLOR_CHANGED
    else:
        msg = 'ok'
        color = C.COLOR_OK
    if delegated_vars:
        msg += (': [%s -> %s]' % (result._host.get_name(), delegated_vars['ansible_host']))
    else:
        msg += (': [%s]' % result._host.get_name())
    msg += (' => (item=%s)' % (self._get_item_label(result._result),))
    if (((self._display.verbosity > 0) or ('_ansible_verbose_always' in result._result)) and ('_ansible_verbose_override' not in result._result)):
        msg += (' => %s' % self._dump_results(result._result))
    self._display.display(msg, color=color)