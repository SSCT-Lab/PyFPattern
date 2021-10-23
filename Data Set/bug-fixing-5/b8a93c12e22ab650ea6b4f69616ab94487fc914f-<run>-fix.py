def run(self, tmp=None, task_vars=None):
    ' handler for aws_s3 operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    del tmp
    source = self._task.args.get('src', None)
    try:
        new_module_args = self._task.args.copy()
        if source:
            source = os.path.expanduser(source)
            if (not self._remote_file_exists(source)):
                try:
                    source = self._loader.get_real_file(self._find_needle('files', source))
                    new_module_args['src'] = source
                except AnsibleFileNotFound as e:
                    new_module_args['src'] = source
                except AnsibleError as e:
                    raise AnsibleActionFail(to_text(e))
        result.update(self._execute_module(module_args=new_module_args, task_vars=task_vars))
    except AnsibleAction as e:
        result.update(e.result)
    return result