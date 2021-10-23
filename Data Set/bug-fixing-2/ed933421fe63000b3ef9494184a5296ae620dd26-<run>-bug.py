

def run(self, tmp=None, task_vars=None):
    ' handler for template operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    source = self._task.args.get('src', None)
    dest = self._task.args.get('dest', None)
    force = boolean(self._task.args.get('force', True))
    state = self._task.args.get('state', None)
    if (state is not None):
        result['failed'] = True
        result['msg'] = "'state' cannot be specified on a template"
    elif ((source is None) or (dest is None)):
        result['failed'] = True
        result['msg'] = 'src and dest are required'
    else:
        try:
            source = self._find_needle('templates', source)
        except AnsibleError as e:
            result['failed'] = True
            result['msg'] = to_native(e)
    if ('failed' in result):
        return result
    dest = self._remote_expand_user(dest)
    directory_prepended = False
    if dest.endswith(os.sep):
        directory_prepended = True
        base = os.path.basename(source)
        dest = os.path.join(dest, base)
    b_source = to_bytes(source)
    try:
        with open(b_source, 'r') as f:
            template_data = to_text(f.read())
        try:
            template_uid = pwd.getpwuid(os.stat(b_source).st_uid).pw_name
        except:
            template_uid = os.stat(b_source).st_uid
        temp_vars = task_vars.copy()
        temp_vars['template_host'] = os.uname()[1]
        temp_vars['template_path'] = source
        temp_vars['template_mtime'] = datetime.datetime.fromtimestamp(os.path.getmtime(b_source))
        temp_vars['template_uid'] = template_uid
        temp_vars['template_fullpath'] = os.path.abspath(source)
        temp_vars['template_run_date'] = datetime.datetime.now()
        managed_default = C.DEFAULT_MANAGED_STR
        managed_str = managed_default.format(host=temp_vars['template_host'], uid=temp_vars['template_uid'], file=to_bytes(temp_vars['template_path']))
        temp_vars['ansible_managed'] = time.strftime(managed_str, time.localtime(os.path.getmtime(b_source)))
        searchpath = [self._loader._basedir, os.path.dirname(source)]
        if (self._task._role is not None):
            if C.DEFAULT_ROLES_PATH:
                searchpath[:0] = C.DEFAULT_ROLES_PATH
            searchpath.insert(1, self._task._role._role_path)
        self._templar.environment.loader.searchpath = searchpath
        old_vars = self._templar._available_variables
        self._templar.set_available_variables(temp_vars)
        resultant = self._templar.do_template(template_data, preserve_trailing_newlines=True, escape_backslashes=False)
        self._templar.set_available_variables(old_vars)
    except Exception as e:
        result['failed'] = True
        result['msg'] = ((type(e).__name__ + ': ') + str(e))
        return result
    remote_user = (task_vars.get('ansible_ssh_user') or self._play_context.remote_user)
    if (not tmp):
        tmp = self._make_tmp_path(remote_user)
        self._cleanup_remote_tmp = True
    local_checksum = checksum_s(resultant)
    remote_checksum = self.get_checksum(dest, task_vars, (not directory_prepended), source=source, tmp=tmp)
    if isinstance(remote_checksum, dict):
        result.update(remote_checksum)
        return result
    diff = {
        
    }
    new_module_args = self._task.args.copy()
    if ((remote_checksum == '1') or (force and (local_checksum != remote_checksum))):
        result['changed'] = True
        if self._play_context.diff:
            diff = self._get_diff_data(dest, resultant, task_vars, source_file=False)
        if (not self._play_context.check_mode):
            xfered = self._transfer_data(self._connection._shell.join_path(tmp, 'source'), resultant)
            self._fixup_perms2((tmp, xfered), remote_user)
            new_module_args.update(dict(src=xfered, dest=dest, original_basename=os.path.basename(source), follow=True))
            result.update(self._execute_module(module_name='copy', module_args=new_module_args, task_vars=task_vars, tmp=tmp, delete_remote_tmp=False))
        if (result.get('changed', False) and self._play_context.diff):
            result['diff'] = diff
    else:
        new_module_args.update(dict(src=None, original_basename=os.path.basename(source), follow=True))
        result.update(self._execute_module(module_name='file', module_args=new_module_args, task_vars=task_vars, tmp=tmp, delete_remote_tmp=False))
    self._remove_tmp_path(tmp)
    return result
