def _build_test_case(self, task_data, host_data):
    ' build a TestCase from the given TaskData and HostData '
    name = ('[%s] %s: %s' % (host_data.name, task_data.play, task_data.name))
    duration = (host_data.finish - task_data.start)
    if (host_data.status == 'included'):
        return TestCase(name, task_data.path, duration, host_data.result)
    res = host_data.result._result
    rc = res.get('rc', 0)
    dump = self._dump_results(res, indent=0)
    if (host_data.status == 'ok'):
        return TestCase(name, task_data.path, duration, dump)
    test_case = TestCase(name, task_data.path, duration)
    if (host_data.status == 'failed'):
        if ('exception' in res):
            message = res['exception'].strip().split('\n')[(- 1)]
            output = res['exception']
            test_case.add_error_info(message, output)
        elif ('msg' in res):
            message = res['msg']
            test_case.add_failure_info(message, dump)
        else:
            test_case.add_failure_info(('rc=%s' % rc), dump)
    elif (host_data.status == 'skipped'):
        if ('skip_reason' in res):
            message = res['skip_reason']
        else:
            message = 'skipped'
        test_case.add_skipped_info(message)
    return test_case