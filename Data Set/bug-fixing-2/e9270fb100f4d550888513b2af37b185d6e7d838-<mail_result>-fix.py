

def mail_result(self, result, failtype):
    host = result._host.get_name()
    if (not self.sender):
        self.sender = ('"Ansible: %s" <root>' % host)
    if self.itembody:
        subject = self.itemsubject
    elif (result._result.get('failed_when_result') is True):
        subject = "Failed due to 'failed_when' condition"
    elif result._result.get('msg'):
        subject = self.subject_msg(result._result['msg'], failtype, 0)
    elif result._result.get('stderr'):
        subject = self.subject_msg(result._result['stderr'], failtype, (- 1))
    elif result._result.get('stdout'):
        subject = self.subject_msg(result._result['stdout'], failtype, (- 1))
    elif result._result.get('exception'):
        subject = self.subject_msg(result._result['exception'], failtype, (- 1))
    else:
        subject = ('%s: %s' % (failtype, (result._task.name or result._task.action)))
    body = ('Playbook: %s\n' % os.path.basename(self.playbook._file_name))
    if result._task.name:
        body += ('Task: %s\n' % result._task.name)
    body += ('Module: %s\n' % result._task.action)
    body += ('Host: %s\n' % host)
    body += '\n'
    body += 'The following task failed:\n\n'
    if ('invocation' in result._result):
        body += self.indent(('%s: %s\n' % (result._task.action, json.dumps(result._result['invocation']['module_args'], indent=4))))
    elif result._task.name:
        body += self.indent(('%s (%s)\n' % (result._task.name, result._task.action)))
    else:
        body += self.indent(('%s\n' % result._task.action))
    body += '\n'
    if self.itembody:
        body += self.itembody
    elif (result._result.get('failed_when_result') is True):
        body += (('due to the following condition:\n\n' + self.indent(('failed_when:\n- ' + '\n- '.join(result._task.failed_when)))) + '\n\n')
    elif result._result.get('msg'):
        body += self.body_blob(result._result['msg'], 'message')
    if result._result.get('stdout'):
        body += self.body_blob(result._result['stdout'], 'standard output')
    if result._result.get('stderr'):
        body += self.body_blob(result._result['stderr'], 'error output')
    if result._result.get('exception'):
        body += self.body_blob(result._result['exception'], 'exception')
    if result._result.get('warnings'):
        for i in range(len(result._result.get('warnings'))):
            body += self.body_blob(result._result['warnings'][i], ('exception %d' % (i + 1)))
    if result._result.get('deprecations'):
        for i in range(len(result._result.get('deprecations'))):
            body += self.body_blob(result._result['deprecations'][i], ('exception %d' % (i + 1)))
    body += 'and a complete dump of the error:\n\n'
    body += self.indent(('%s: %s' % (failtype, json.dumps(result._result, indent=4))))
    self.mail(subject=subject, body=body)
