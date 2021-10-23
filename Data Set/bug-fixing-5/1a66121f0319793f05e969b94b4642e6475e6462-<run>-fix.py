def run(self, task_vars=None):
    config_module = (hasattr(self, '_config_module') and self._config_module)
    if (config_module and self._task.args.get('src')):
        try:
            self._handle_src_option()
        except AnsibleError as e:
            return {
                'failed': True,
                'msg': e.message,
                'changed': False,
            }
    result = super(ActionModule, self).run(task_vars=task_vars)
    if (config_module and self._task.args.get('backup') and (not result.get('failed'))):
        self._handle_backup_option(result, task_vars)
    return result