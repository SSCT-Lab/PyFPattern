def v2_runner_on_unreachable(self, result):
    if ((self._play.strategy == 'free') and (self._last_task_banner != result._task._uuid)):
        self._print_task_banner(result._task)
    delegated_vars = result._result.get('_ansible_delegated_vars', None)
    if delegated_vars:
        self._display.display(('fatal: [%s -> %s]: UNREACHABLE! => %s' % (result._host.get_name(), delegated_vars['ansible_host'], self._dump_results(result._result))), color=C.COLOR_UNREACHABLE)
    else:
        self._display.display(('fatal: [%s]: UNREACHABLE! => %s' % (result._host.get_name(), self._dump_results(result._result))), color=C.COLOR_UNREACHABLE)