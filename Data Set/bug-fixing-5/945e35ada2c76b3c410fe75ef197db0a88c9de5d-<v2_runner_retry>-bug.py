def v2_runner_retry(self, result):
    msg = ('  Retrying... (%d of %d)' % (result._result['attempts'], result._result['retries']))
    if self._run_is_verbose(result, verbosity=2):
        msg += ('Result was: %s' % self._dump_results(result._result))
    self._display.display(msg, color=C.COLOR_DEBUG)