def v2_runner_on_ok(self, result, **kwargs):
    'Run when a task finishes correctly.'
    failed = ('failed' in result._result)
    unreachable = ('unreachable' in result._result)
    if (('print_action' in result._task.tags) or failed or unreachable or (self._display.verbosity > 1)):
        self._print_task()
        self.last_skipped = False
        msg = (to_text(result._result.get('msg', '')) or to_text(result._result.get('reason', '')))
        self._print_host_or_item(result._host, result._result.get('changed', False), msg, result._result.get('diff', None), is_host=True, error=(failed or unreachable), stdout=result._result.get('module_stdout', None), stderr=result._result.get('exception', None))
        if ('results' in result._result):
            for r in result._result['results']:
                failed = ('failed' in r)
                self._print_host_or_item(r['item'], r.get('changed', False), to_text(r.get('msg', '')), r.get('diff', None), is_host=False, error=failed, stdout=r.get('module_stdout', None), stderr=r.get('exception', None))
    else:
        self.last_skipped = True
        print('.', end='')