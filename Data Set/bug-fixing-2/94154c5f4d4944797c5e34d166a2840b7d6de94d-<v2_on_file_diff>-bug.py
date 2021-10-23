

def v2_on_file_diff(self, result):
    if (self._last_task_banner != result._task._uuid):
        self._print_task_banner(result._task)
    if (result._task.loop and ('results' in result._result)):
        for res in result._result['results']:
            if (('diff' in res) and res['diff'] and res.get('changed', False)):
                diff = self._get_diff(res['diff'])
                if diff:
                    self._display.display(diff)
    elif (('diff' in result._result) and result._result['diff'] and result._result.get('changed', False)):
        diff = self._get_diff(result._result['diff'])
        if diff:
            self._display.display(diff)
