

def v2_runner_on_ok(self, result):
    self._clean_results(result._result, result._task.action)
    self._handle_warnings(result._result)
    if result._result.get('changed', False):
        color = C.COLOR_CHANGED
        state = 'CHANGED'
    else:
        color = C.COLOR_OK
        state = 'SUCCESS'
    if (result._task.action in C.MODULE_NO_JSON):
        self._display.display(self._command_generic_msg(result._host.get_name(), result._result, state), color=color)
    else:
        self._display.display(('%s | %s => %s' % (result._host.get_name(), state, self._dump_results(result._result, indent=4))), color=color)
