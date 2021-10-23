def v2_runner_on_ok(self, result):
    if (result._task.action in C.MODULE_NO_JSON):
        self._display.display(self._command_generic_msg(result._host.get_name(), result._result, 'SUCCESS'), color=C.COLOR_OK)
    else:
        self._display.display(('%s | SUCCESS => %s' % (result._host.get_name(), self._dump_results(result._result, indent=0).replace('\n', ''))), color=C.COLOR_OK)