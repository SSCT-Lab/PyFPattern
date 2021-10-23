def v2_runner_on_ok(self, result):
    if (not self._plugin_options.get('display_ok_hosts', DEFAULT_DISPLAY_OK_HOSTS)):
        return
    delegated_vars = result._result.get('_ansible_delegated_vars', None)
    if (self._last_task_banner != result._task._uuid):
        self._print_task_banner(result._task)
    if isinstance(result._task, TaskInclude):
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
    self._handle_warnings(result._result)
    if (result._task.loop and ('results' in result._result)):
        self._process_items(result)
    else:
        self._clean_results(result._result, result._task.action)
        if (((self._display.verbosity > 0) or ('_ansible_verbose_always' in result._result)) and ('_ansible_verbose_override' not in result._result)):
            msg += (' => %s' % (self._dump_results(result._result),))
        self._display.display(msg, color=color)