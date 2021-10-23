

def run(self, tmp=None, task_vars=None):
    ' handler for unarchive operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    source = self._task.args.get('src', None)
    dest = self._task.args.get('dest', None)
    remote_src = boolean(self._task.args.get('remote_src', False), strict=False)
    creates = self._task.args.get('creates', None)
    decrypt = self._task.args.get('decrypt', True)
    if ('copy' in self._task.args):
        if ('remote_src' in self._task.args):
            result['failed'] = True
            result['msg'] = "parameters are mutually exclusive: ('copy', 'remote_src')"
            return result
        self._task.args['remote_src'] = remote_src = (not boolean(self._task.args.pop('copy'), strict=False))
    if ((source is None) or (dest is None)):
        result['failed'] = True
        result['msg'] = 'src (or content) and dest are required'
        return result
    if (not tmp):
        tmp = self._make_tmp_path()
    if creates:
        creates = self._remote_expand_user(creates)
        if self._remote_file_exists(creates):
            result['skipped'] = True
            result['msg'] = ('skipped, since %s exists' % creates)
            self._remove_tmp_path(tmp)
            return result
    dest = self._remote_expand_user(dest)
    source = os.path.expanduser(source)
    if (not remote_src):
        try:
            source = self._loader.get_real_file(self._find_needle('files', source), decrypt=decrypt)
        except AnsibleError as e:
            result['failed'] = True
            result['msg'] = to_text(e)
            self._remove_tmp_path(tmp)
            return result
    try:
        remote_stat = self._execute_remote_stat(dest, all_vars=task_vars, follow=True)
    except AnsibleError as e:
        result['failed'] = True
        result['msg'] = to_text(e)
        self._remove_tmp_path(tmp)
        return result
    if ((not remote_stat['exists']) or (not remote_stat['isdir'])):
        result['failed'] = True
        result['msg'] = ("dest '%s' must be an existing dir" % dest)
        self._remove_tmp_path(tmp)
        return result
    if (not remote_src):
        tmp_src = self._connection._shell.join_path(tmp, 'source')
        self._transfer_file(source, tmp_src)
    if (not remote_src):
        self._fixup_perms2((tmp, tmp_src))
        new_module_args = self._task.args.copy()
        new_module_args.update(dict(src=tmp_src, original_basename=os.path.basename(source)))
    else:
        new_module_args = self._task.args.copy()
        new_module_args.update(dict(original_basename=os.path.basename(source)))
    for key in ('decrypt',):
        if (key in new_module_args):
            del new_module_args[key]
    result.update(self._execute_module(module_args=new_module_args, task_vars=task_vars))
    self._remove_tmp_path(tmp)
    return result
