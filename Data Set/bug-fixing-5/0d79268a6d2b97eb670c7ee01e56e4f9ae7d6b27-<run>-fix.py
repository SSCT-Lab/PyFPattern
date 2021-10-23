def run(self, tmp=None, task_vars=None):
    if self._task.args.get('src'):
        try:
            self._handle_template()
        except ValueError as exc:
            return dict(failed=True, msg=exc.message)
    result = super(ActionModule, self).run(tmp, task_vars)
    del tmp
    if (self._task.args.get('backup') and result.get('__backup__')):
        filepath = self._write_backup(task_vars['inventory_hostname'], result['__backup__'])
        result['backup_path'] = filepath
    for key in list(result.keys()):
        if PRIVATE_KEYS_RE.match(key):
            del result[key]
    return result