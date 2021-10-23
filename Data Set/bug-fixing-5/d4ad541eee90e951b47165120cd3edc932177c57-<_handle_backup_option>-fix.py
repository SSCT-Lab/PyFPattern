def _handle_backup_option(self, result, task_vars):
    filename = None
    backup_path = None
    try:
        content = result['__backup__']
    except KeyError:
        raise AnsibleError('Failed while reading configuration backup')
    backup_options = self._task.args.get('backup_options')
    if backup_options:
        filename = backup_options.get('filename')
        backup_path = backup_options.get('dir_path')
    if (not backup_path):
        cwd = self._get_working_path()
        backup_path = os.path.join(cwd, 'backup')
    if (not filename):
        tstamp = time.strftime('%Y-%m-%d@%H:%M:%S', time.localtime(time.time()))
        filename = ('%s_config.%s' % (task_vars['inventory_hostname'], tstamp))
    dest = os.path.join(backup_path, filename)
    backup_path = os.path.expanduser(os.path.expandvars(to_bytes(backup_path, errors='surrogate_or_strict')))
    if (not os.path.exists(backup_path)):
        os.makedirs(backup_path)
    new_task = self._task.copy()
    for item in self._task.args:
        if (not item.startswith('_')):
            new_task.args.pop(item, None)
    new_task.args.update(dict(content=content, dest=dest))
    copy_action = self._shared_loader_obj.action_loader.get('copy', task=new_task, connection=self._connection, play_context=self._play_context, loader=self._loader, templar=self._templar, shared_loader_obj=self._shared_loader_obj)
    copy_result = copy_action.run(task_vars=task_vars)
    if copy_result.get('failed'):
        result['failed'] = copy_result['failed']
        result['msg'] = copy_result.get('msg')
        return
    result['backup_path'] = dest
    if copy_result.get('changed', False):
        result['changed'] = copy_result['changed']
    if (backup_options and backup_options.get('filename')):
        result['date'] = time.strftime('%Y-%m-%d', time.gmtime(os.stat(result['backup_path']).st_ctime))
        result['time'] = time.strftime('%H:%M:%S', time.gmtime(os.stat(result['backup_path']).st_ctime))
    else:
        result['date'] = tstamp.split('@')[0]
        result['time'] = tstamp.split('@')[1]
        result['shortname'] = result['backup_path'][::(- 1)].split('.', 1)[1][::(- 1)]
        result['filename'] = result['backup_path'].split('/')[(- 1)]
    for key in list(result.keys()):
        if PRIVATE_KEYS_RE.match(key):
            del result[key]