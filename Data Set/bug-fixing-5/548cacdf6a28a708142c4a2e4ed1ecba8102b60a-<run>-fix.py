def run(self, tmp=None, task_vars=None):
    ' handler for template operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    source = self._task.args.get('src', None)
    dest = self._task.args.get('dest', None)
    force = boolean(self._task.args.get('force', True))
    state = self._task.args.get('state', None)
    newline_sequence = self._task.args.get('newline_sequence', self.DEFAULT_NEWLINE_SEQUENCE)
    variable_start_string = self._task.args.get('variable_start_string', None)
    variable_end_string = self._task.args.get('variable_end_string', None)
    block_start_string = self._task.args.get('block_start_string', None)
    block_end_string = self._task.args.get('block_end_string', None)
    trim_blocks = self._task.args.get('trim_blocks', None)
    wrong_sequences = ['\\n', '\\r', '\\r\\n']
    allowed_sequences = ['\n', '\r', '\r\n']
    if (newline_sequence in wrong_sequences):
        newline_sequence = allowed_sequences[wrong_sequences.index(newline_sequence)]
    if (state is not None):
        result['failed'] = True
        result['msg'] = "'state' cannot be specified on a template"
    elif ((source is None) or (dest is None)):
        result['failed'] = True
        result['msg'] = 'src and dest are required'
    elif (newline_sequence not in allowed_sequences):
        result['failed'] = True
        result['msg'] = 'newline_sequence needs to be one of: \n, \r or \r\n'
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
        dest = self._connection._shell.join_path(dest, os.path.basename(source))
    else:
        dest_stat = self._execute_remote_stat(dest, task_vars, True, tmp=tmp)
        if (dest_stat['exists'] and dest_stat['isdir']):
            dest = self._connection._shell.join_path(dest, os.path.basename(source))
    b_source = to_bytes(source)
    try:
        with open(b_source, 'r') as f:
            template_data = to_text(f.read())
        searchpath = task_vars.get('ansible_search_path', [])
        searchpath.extend([self._loader._basedir, os.path.dirname(source)])
        newsearchpath = []
        for p in searchpath:
            newsearchpath.append(os.path.join(p, 'templates'))
            newsearchpath.append(p)
        searchpath = newsearchpath
        self._templar.environment.loader.searchpath = searchpath
        self._templar.environment.newline_sequence = newline_sequence
        if (block_start_string is not None):
            self._templar.environment.block_start_string = block_start_string
        if (block_end_string is not None):
            self._templar.environment.block_end_string = block_end_string
        if (variable_start_string is not None):
            self._templar.environment.variable_start_string = variable_start_string
        if (variable_end_string is not None):
            self._templar.environment.variable_end_string = variable_end_string
        if (trim_blocks is not None):
            self._templar.environment.trim_blocks = bool(trim_blocks)
        temp_vars = task_vars.copy()
        temp_vars.update(generate_ansible_template_vars(source))
        old_vars = self._templar._available_variables
        self._templar.set_available_variables(temp_vars)
        resultant = self._templar.do_template(template_data, preserve_trailing_newlines=True, escape_backslashes=False)
        self._templar.set_available_variables(old_vars)
    except Exception as e:
        result['failed'] = True
        result['msg'] = ((type(e).__name__ + ': ') + str(e))
        return result
    if (not tmp):
        tmp = self._make_tmp_path()
    local_checksum = checksum_s(resultant)
    remote_checksum = self.get_checksum(dest, task_vars, (not directory_prepended), source=source, tmp=tmp)
    if isinstance(remote_checksum, dict):
        result.update(remote_checksum)
        return result
    diff = {
        
    }
    new_module_args = self._task.args.copy()
    new_module_args.pop('newline_sequence', None)
    new_module_args.pop('block_start_string', None)
    new_module_args.pop('block_end_string', None)
    new_module_args.pop('variable_start_string', None)
    new_module_args.pop('variable_end_string', None)
    new_module_args.pop('trim_blocks', None)
    if ((remote_checksum == '1') or (force and (local_checksum != remote_checksum))):
        result['changed'] = True
        if self._play_context.diff:
            diff = self._get_diff_data(dest, resultant, task_vars, source_file=False)
        if (not self._play_context.check_mode):
            xfered = self._transfer_data(self._connection._shell.join_path(tmp, 'source'), resultant)
            self._fixup_perms2((tmp, xfered))
            new_module_args.update(dict(src=xfered, dest=dest, original_basename=os.path.basename(source), follow=True))
            result.update(self._execute_module(module_name='copy', module_args=new_module_args, task_vars=task_vars, tmp=tmp, delete_remote_tmp=False))
        if (result.get('changed', False) and self._play_context.diff):
            result['diff'] = diff
    else:
        new_module_args.update(dict(src=None, original_basename=os.path.basename(source), follow=True))
        result.update(self._execute_module(module_name='file', module_args=new_module_args, task_vars=task_vars, tmp=tmp, delete_remote_tmp=False))
    self._remove_tmp_path(tmp)
    return result