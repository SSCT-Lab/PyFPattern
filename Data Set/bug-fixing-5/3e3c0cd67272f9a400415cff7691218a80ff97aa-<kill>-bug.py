def kill(self):
    '\n        Kill the process launched to process the file, and ensure consistent state.\n        '
    if (self._process is None):
        raise AirflowException('Tried to kill before starting!')
    self._result_queue = None
    self._kill_process()
    self._manager.shutdown()