def v2_runner_on_failed(self, result, ignore_errors=False):
    delegated_vars = result._result.get('_ansible_delegated_vars', None)
    self._clean_results(result._result, result._task.action)
    if (self._last_task_banner != result._task._uuid):
        self._print_task_banner(result._task)
    use_stderr = self._plugin_options.get('display_failed_stderr', DEFAULT_DISPLAY_FAILED_STDERR)
    self._handle_exception(result._result, use_stderr=use_stderr)
    self._handle_warnings(result._result)
    if (result._task.loop and ('results' in result._result)):
        self._process_items(result)
    elif delegated_vars:
        self._display.display(('fatal: [%s -> %s]: FAILED! => %s' % (result._host.get_name(), delegated_vars['ansible_host'], self._dump_results(result._result))), color=C.COLOR_ERROR, stderr=use_stderr)
    else:
        self._display.display(('fatal: [%s]: FAILED! => %s' % (result._host.get_name(), self._dump_results(result._result))), color=C.COLOR_ERROR, stderr=use_stderr)
    if ignore_errors:
        self._display.display('...ignoring', color=C.COLOR_SKIP)