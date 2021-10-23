def run(self, tmp=None, task_vars=None):
    if (task_vars is None):
        task_vars = dict()
    for arg in self._task.args:
        if (arg not in self.VALID_ARGS):
            return {
                'failed': True,
                'msg': ("'%s' is not a valid option in debug" % arg),
            }
    if (('msg' in self._task.args) and ('var' in self._task.args)):
        return {
            'failed': True,
            'msg': "'msg' and 'var' are incompatible options",
        }
    result = super(ActionModule, self).run(tmp, task_vars)
    verbosity = 0
    if ('verbosity' in self._task.args):
        verbosity = int(self._task.args['verbosity'])
    if (verbosity <= self._display.verbosity):
        if ('msg' in self._task.args):
            result['msg'] = self._task.args['msg']
        elif ('var' in self._task.args):
            try:
                results = self._templar.template(self._task.args['var'], convert_bare=True, fail_on_undefined=True, bare_deprecated=False)
                if (results == self._task.args['var']):
                    if (type(results) not in [str, unicode]):
                        raise AnsibleUndefinedVariable
                    results = self._templar.template((('{{' + results) + '}}'), convert_bare=True, fail_on_undefined=True)
            except AnsibleUndefinedVariable:
                results = 'VARIABLE IS NOT DEFINED!'
            if (type(self._task.args['var']) in (list, dict)):
                result[to_unicode(type(self._task.args['var']))] = results
            else:
                result[self._task.args['var']] = results
        else:
            result['msg'] = 'Hello world!'
        result['_ansible_verbose_always'] = True
    else:
        result['skipped_reason'] = 'Verbosity threshold not met.'
        result['skipped'] = True
    return result