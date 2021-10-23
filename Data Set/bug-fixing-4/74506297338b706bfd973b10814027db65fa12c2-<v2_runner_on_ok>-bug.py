def v2_runner_on_ok(self, result):
    delegated_vars = result._result.get('_ansible_delegated_vars', None)
    self._clean_results(result._result, result._task.action)
    if (result._task.action in ('include', 'include_role')):
        return
    elif result._result.get('changed', False):
        if delegated_vars:
            msg = ('changed: [%s -> %s]' % (result._host.get_name(), delegated_vars['ansible_host']))
        else:
            msg = ('changed: [%s]' % result._host.get_name())
        color = C.COLOR_CHANGED
    else:
        if delegated_vars:
            msg = ('ok: [%s -> %s]' % (result._host.get_name(), delegated_vars['ansible_host']))
        else:
            msg = ('ok: [%s]' % result._host.get_name())
        color = C.COLOR_OK
    if (result._task.loop and ('results' in result._result)):
        self._process_items(result)
    else:
        if (((self._display.verbosity > 0) or ('_ansible_verbose_always' in result._result)) and (not ('_ansible_verbose_override' in result._result))):
            msg += (' => %s' % (self._dump_results(result._result),))
        self._display.display(msg, color=color)
    self._handle_warnings(result._result)