

def v2_runner_on_unreachable(self, result):
    self._preprocess_result(result)
    msg = 'unreachable'
    display_color = C.COLOR_UNREACHABLE
    task_result = self._process_result_output(result, msg)
    self._display.display(('  ' + task_result), display_color, stderr=self.display_failed_stderr)
