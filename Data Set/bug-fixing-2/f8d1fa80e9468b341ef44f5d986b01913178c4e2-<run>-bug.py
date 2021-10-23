

def run(self, tmp=None, task_vars=None):
    if (task_vars is None):
        task_vars = dict()
    if (('msg' in self._task.args) and ('var' in self._task.args)):
        return {
            'failed': True,
            'msg': "'msg' and 'var' are incompatible options",
        }
    result = super(ActionModule, self).run(tmp, task_vars)
    del tmp
    verbosity = int(self._task.args.get('verbosity', 0))
    if (verbosity <= self._display.verbosity):
        if ('msg' in self._task.args):
            result['msg'] = self._task.args['msg']
        elif ('var' in self._task.args):
            try:
                results = self._templar.template(self._task.args['var'], convert_bare=True, fail_on_undefined=True)
                if (results == self._task.args['var']):
                    if (not isinstance(results, string_types)):
                        raise AnsibleUndefinedVariable
                    results = self._templar.template((('{{' + results) + '}}'), convert_bare=True, fail_on_undefined=True)
            except AnsibleUndefinedVariable as e:
                results = 'VARIABLE IS NOT DEFINED!'
                if (self._display.verbosity > 0):
                    results += (': %s' % to_text(e))
            if isinstance(self._task.args['var'], (list, dict)):
                result[to_text(type(self._task.args['var']))] = results
            else:
                result[self._task.args['var']] = results
        else:
            result['msg'] = 'Hello world!'
        result['_ansible_verbose_always'] = True
    else:
        result['skipped_reason'] = 'Verbosity threshold not met.'
        result['skipped'] = True
    return result
