def v2_runner_on_ok(self, result):
    self._clean_results(result._result, result._task.action)
    self._handle_warnings(result._result)
    if (result._task.action in C.MODULE_NO_JSON):
        self._display.display(self._command_generic_msg(result._host.get_name(), result._result, 'SUCCESS'), color=C.COLOR_OK)
    elif (('changed' in result._result) and result._result['changed']):
        self._display.display(('%s | SUCCESS => %s' % (result._host.get_name(), self._dump_results(result._result, indent=4))), color=C.COLOR_CHANGED)
    else:
        self._display.display(('%s | SUCCESS => %s' % (result._host.get_name(), self._dump_results(result._result, indent=4))), color=C.COLOR_OK)