def v2_runner_on_failed(self, result, ignore_errors=False):
    if ((self._play.strategy == 'free') and (self._last_task_banner != result._task._uuid)):
        self._print_task_banner(result._task)
    delegated_vars = result._result.get('_ansible_delegated_vars', None)
    if ('exception' in result._result):
        if (self._display.verbosity < 3):
            error = result._result['exception'].strip().split('\n')[(- 1)]
            msg = ('An exception occurred during task execution. To see the full traceback, use -vvv. The error was: %s' % error)
        else:
            msg = ('An exception occurred during task execution. The full traceback is:\n' + result._result['exception'])
        self._display.display(msg, color=C.COLOR_ERROR)
    if (result._task.loop and ('results' in result._result)):
        self._process_items(result)
    elif delegated_vars:
        self._display.display(('fatal: [%s -> %s]: FAILED! => %s' % (result._host.get_name(), delegated_vars['ansible_host'], self._dump_results(result._result))), color=C.COLOR_ERROR)
    else:
        self._display.display(('fatal: [%s]: FAILED! => %s' % (result._host.get_name(), self._dump_results(result._result))), color=C.COLOR_ERROR)
    if result._task.ignore_errors:
        self._display.display('...ignoring', color=C.COLOR_SKIP)