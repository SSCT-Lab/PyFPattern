

def run(self, tmp=None, task_vars=None):
    ' handler for template operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    tmp = self._connection._shell.tempdir
    source = self._task.args.get('src', None)
    dest = self._task.args.get('dest', None)
    force = boolean(self._task.args.get('force', True), strict=False)
    follow = boolean(self._task.args.get('follow', False), strict=False)
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
    try:
        if (state is not None):
            raise AnsibleActionFail("'state' cannot be specified on a template")
        elif ((source is None) or (dest is None)):
            raise AnsibleActionFail('src and dest are required')
        elif (newline_sequence not in allowed_sequences):
            raise AnsibleActionFail('newline_sequence needs to be one of: \n, \r or \r\n')
        else:
            try:
                source = self._find_needle('templates', source)
            except AnsibleError as e:
                raise AnsibleActionFail(to_text(e))
        try:
            tmp_source = self._loader.get_real_file(source)
        except AnsibleFileNotFound as e:
            raise AnsibleActionFail(('could not find src=%s, %s' % (source, to_text(e))))
        try:
            with open(tmp_source, 'r') as f:
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
        except AnsibleAction:
            raise
        except Exception as e:
            raise AnsibleActionFail(('%s: %s' % (type(e).__name__, to_text(e))))
        finally:
            self._loader.cleanup_tmp_file(tmp_source)
        new_task = self._task.copy()
        new_task.args.pop('newline_sequence', None)
        new_task.args.pop('block_start_string', None)
        new_task.args.pop('block_end_string', None)
        new_task.args.pop('variable_start_string', None)
        new_task.args.pop('variable_end_string', None)
        new_task.args.pop('trim_blocks', None)
        try:
            tempdir = tempfile.mkdtemp(dir=C.DEFAULT_LOCAL_TMP)
            result_file = os.path.join(tempdir, os.path.basename(source))
            with open(result_file, 'wb') as f:
                f.write(to_bytes(resultant, errors='surrogate_or_strict'))
            new_task.args.update(dict(src=result_file, dest=dest, follow=follow))
            copy_action = self._shared_loader_obj.action_loader.get('copy', task=new_task, connection=self._connection, play_context=self._play_context, loader=self._loader, templar=self._templar, shared_loader_obj=self._shared_loader_obj)
            result.update(copy_action.run(task_vars=task_vars, tmp=tmp))
        finally:
            shutil.rmtree(tempdir)
    except AnsibleAction as e:
        result.update(e.result)
    finally:
        self._remove_tmp_path(tmp)
    return result
