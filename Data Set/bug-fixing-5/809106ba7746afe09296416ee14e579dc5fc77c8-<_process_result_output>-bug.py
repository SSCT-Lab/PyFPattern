def _process_result_output(self, result, msg):
    task_host = result._host.get_name()
    task_result = ('%s %s' % (task_host, msg))
    if self._run_is_verbose(result):
        task_result = ('%s %s: %s' % (task_host, msg, self._dump_results(result._result, indent=4)))
    if self.delegated_vars:
        task_delegate_host = self.delegated_vars['ansible_host']
        task_result = ('%s -> %s %s' % (task_host, task_delegate_host, msg))
    if (result._result.get('msg') and (result._result.get('msg') != 'All items completed')):
        task_result += (' | msg: ' + result._result.get('msg'))
    if result._result.get('stdout'):
        task_result += (' | stdout: ' + result._result.get('stdout'))
    if result._result.get('stderr'):
        task_result += (' | stderr: ' + result._result.get('stderr'))
    return task_result