

def run(self, tmp=None, task_vars=None):
    ' handler for unarchive operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    source = self._task.args.get('src', None)
    dest = self._task.args.get('dest', None)
    remote_src = boolean(self._task.args.get('remote_src', False))
    creates = self._task.args.get('creates', None)
    if ('copy' in self._task.args):
        if ('remote_src' in self._task.args):
            result['failed'] = True
            result['msg'] = "parameters are mutually exclusive: ('copy', 'remote_src')"
            return result
        remote_src = (not boolean(self._task.args.get('copy')))
    if ((source is None) or (dest is None)):
        result['failed'] = True
        result['msg'] = 'src (or content) and dest are required'
        return result
    remote_user = (task_vars.get('ansible_ssh_user') or self._play_context.remote_user)
    if (not tmp):
        tmp = self._make_tmp_path(remote_user)
        self._cleanup_remote_tmp = True
    if creates:
        result = self._execute_module(module_name='stat', module_args=dict(path=creates), task_vars=task_vars)
        stat = result.get('stat', None)
        if (stat and stat.get('exists', False)):
            result['skipped'] = True
            result['msg'] = ('skipped, since %s exists' % creates)
            self._remove_tmp_path(tmp)
            return result
    dest = self._remote_expand_user(dest)
    source = os.path.expanduser(source)
    if (not remote_src):
        try:
            source = self._loader.get_real_file(self._find_needle('files', source))
        except AnsibleError as e:
            result['failed'] = True
            result['msg'] = to_native(e)
            self._remove_tmp_path(tmp)
            return result
    remote_checksum = self._remote_checksum(dest, all_vars=task_vars, follow=True)
    if (remote_checksum == '4'):
        result['failed'] = True
        result['msg'] = "python isn't present on the system.  Unable to compute checksum"
        self._remove_tmp_path(tmp)
        return result
    elif (remote_checksum != '3'):
        result['failed'] = True
        result['msg'] = ("dest '%s' must be an existing dir" % dest)
        self._remove_tmp_path(tmp)
        return result
    if (not remote_src):
        tmp_src = self._connection._shell.join_path(tmp, 'source')
        self._transfer_file(source, tmp_src)
    if (not remote_src):
        self._fixup_perms2((tmp, tmp_src), remote_user)
        new_module_args = self._task.args.copy()
        new_module_args.update(dict(src=tmp_src, original_basename=os.path.basename(source)))
    else:
        new_module_args = self._task.args.copy()
        new_module_args.update(dict(original_basename=os.path.basename(source)))
    result.update(self._execute_module(module_args=new_module_args, task_vars=task_vars))
    self._remove_tmp_path(tmp)
    return result
