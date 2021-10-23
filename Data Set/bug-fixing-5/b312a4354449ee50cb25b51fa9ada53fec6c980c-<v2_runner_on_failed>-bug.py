def v2_runner_on_failed(self, res, ignore_errors=False):
    host = res._host.get_name()
    if ignore_errors:
        return
    sender = ('"Ansible: %s" <root>' % host)
    attach = res._task.action
    if ('invocation' in res._result):
        attach = ('%s:  %s' % (res._result['invocation']['module_name'], json.dumps(res._result['invocation']['module_args'])))
    subject = ('Failed: %s' % attach)
    body = (('The following task failed for host ' + host) + (':\n\n%s\n\n' % attach))
    if (('stdout' in res._result.keys()) and res._result['stdout']):
        subject = res._result['stdout'].strip('\r\n').split('\n')[(- 1)]
        body += (('with the following output in standard output:\n\n' + res._result['stdout']) + '\n\n')
    if (('stderr' in res._result.keys()) and res._result['stderr']):
        subject = res['stderr'].strip('\r\n').split('\n')[(- 1)]
        body += (('with the following output in standard error:\n\n' + res._result['stderr']) + '\n\n')
    if (('msg' in res._result.keys()) and res._result['msg']):
        subject = res._result['msg'].strip('\r\n').split('\n')[0]
        body += (('with the following message:\n\n' + res._result['msg']) + '\n\n')
    body += ('A complete dump of the error:\n\n' + self._dump_results(res._result))
    mail(sender=sender, subject=subject, body=body)