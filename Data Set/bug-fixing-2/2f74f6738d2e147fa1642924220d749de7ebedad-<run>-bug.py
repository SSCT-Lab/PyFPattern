

def run(self, tmp=None, task_vars=None):
    ' handler for file transfer operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    source = self._task.args.get('src', None)
    content = self._task.args.get('content', None)
    dest = self._task.args.get('dest', None)
    raw = boolean(self._task.args.get('raw', 'no'))
    force = boolean(self._task.args.get('force', 'yes'))
    faf = self._task.first_available_file
    remote_src = boolean(self._task.args.get('remote_src', False))
    follow = boolean(self._task.args.get('follow', False))
    if (((source is None) and (content is None) and (faf is None)) or (dest is None)):
        result['failed'] = True
        result['msg'] = 'src (or content) and dest are required'
        return result
    elif (((source is not None) or (faf is not None)) and (content is not None)):
        result['failed'] = True
        result['msg'] = 'src and content are mutually exclusive'
        return result
    elif ((content is not None) and (dest is not None) and dest.endswith('/')):
        result['failed'] = True
        result['msg'] = 'dest must be a file if content is defined'
        return result
    source_trailing_slash = False
    if source:
        source_trailing_slash = self._connection._shell.path_has_trailing_slash(source)
    content_tempfile = None
    if (content is not None):
        try:
            if (isinstance(content, dict) or isinstance(content, list)):
                content_tempfile = self._create_content_tempfile(json.dumps(content))
            else:
                content_tempfile = self._create_content_tempfile(content)
            source = content_tempfile
        except Exception as err:
            result['failed'] = True
            result['msg'] = ('could not write content temp file: %s' % err)
            return result
    elif faf:
        source = self._get_first_available_file(faf, task_vars.get('_original_file', None))
        if (source is None):
            result['failed'] = True
            result['msg'] = 'could not find src in first_available_file list'
            return result
    elif remote_src:
        result.update(self._execute_module(module_name='copy', module_args=self._task.args, task_vars=task_vars, delete_remote_tmp=False))
        return result
    elif (self._task._role is not None):
        source = self._loader.path_dwim_relative(self._task._role._role_path, 'files', source)
    else:
        source = self._loader.path_dwim_relative(self._loader.get_basedir(), 'files', source)
    source_files = []
    if os.path.isdir(source):
        if source_trailing_slash:
            sz = len(source)
        else:
            sz = (len(source.rsplit('/', 1)[0]) + 1)
        for (base_path, sub_folders, files) in os.walk(source):
            for file in files:
                full_path = os.path.join(base_path, file)
                rel_path = full_path[sz:]
                if rel_path.startswith('/'):
                    rel_path = rel_path[1:]
                source_files.append((full_path, rel_path))
        if (not self._connection._shell.path_has_trailing_slash(dest)):
            dest = self._connection._shell.join_path(dest, '')
    else:
        source_files.append((source, os.path.basename(source)))
    changed = False
    module_return = dict(changed=False)
    module_executed = False
    delete_remote_tmp = (len(source_files) == 1)
    if (not delete_remote_tmp):
        if ((tmp is None) or ('-tmp-' not in tmp)):
            tmp = self._make_tmp_path()
    dest = self._remote_expand_user(dest)
    diffs = []
    for (source_full, source_rel) in source_files:
        local_checksum = checksum(source_full)
        if (local_checksum is None):
            result['failed'] = True
            result['msg'] = ('could not find src=%s' % source_full)
            return result
        if self._connection._shell.path_has_trailing_slash(dest):
            dest_file = self._connection._shell.join_path(dest, source_rel)
        else:
            dest_file = self._connection._shell.join_path(dest)
        dest_status = self._execute_remote_stat(dest_file, all_vars=task_vars, follow=follow)
        if (dest_status['exists'] and dest_status['isdir']):
            if (content is not None):
                self._remove_tempfile_if_content_defined(content, content_tempfile)
                result['failed'] = True
                result['msg'] = 'can not use content with a dir as dest'
                return result
            else:
                dest_file = self._connection._shell.join_path(dest, source_rel)
                dest_status = self._execute_remote_stat(dest_file, all_vars=task_vars, follow=follow)
        if ((not dest_status['exists']) and (not force)):
            continue
        if (local_checksum != dest_status['checksum']):
            changed = True
            if delete_remote_tmp:
                if ((tmp is None) or ('-tmp-' not in tmp)):
                    tmp = self._make_tmp_path()
            if (self._play_context.diff and (not raw)):
                diffs.append(self._get_diff_data(dest_file, source_full, task_vars))
            if self._play_context.check_mode:
                self._remove_tempfile_if_content_defined(content, content_tempfile)
                changed = True
                module_return = dict(changed=True)
                continue
            tmp_src = self._connection._shell.join_path(tmp, 'source')
            if (not raw):
                self._connection.put_file(source_full, tmp_src)
            else:
                self._connection.put_file(source_full, dest_file)
            self._remove_tempfile_if_content_defined(content, content_tempfile)
            if (self._play_context.become and (self._play_context.become_user != 'root')):
                self._remote_chmod('a+r', tmp_src)
            if raw:
                continue
            new_module_args = self._task.args.copy()
            new_module_args.update(dict(src=tmp_src, dest=dest, original_basename=source_rel))
            module_return = self._execute_module(module_name='copy', module_args=new_module_args, task_vars=task_vars, delete_remote_tmp=delete_remote_tmp)
            module_executed = True
        else:
            self._remove_tempfile_if_content_defined(content, content_tempfile)
            if raw:
                self._remove_tmp_path(tmp)
                continue
            new_module_args = self._task.args.copy()
            new_module_args.update(dict(src=source_rel, dest=dest, original_basename=source_rel))
            module_return = self._execute_module(module_name='file', module_args=new_module_args, task_vars=task_vars, delete_remote_tmp=delete_remote_tmp)
            module_executed = True
        if (not module_return.get('checksum')):
            module_return['checksum'] = local_checksum
        if module_return.get('failed'):
            result.update(module_return)
            return result
        if module_return.get('changed'):
            changed = True
        if (('path' in module_return) and ('dest' not in module_return)):
            module_return['dest'] = module_return['path']
    if (((not C.DEFAULT_KEEP_REMOTE_FILES) and (not delete_remote_tmp)) or ((not C.DEFAULT_KEEP_REMOTE_FILES) and delete_remote_tmp and (not module_executed))):
        self._remove_tmp_path(tmp)
    if (module_executed and (len(source_files) == 1)):
        result.update(module_return)
    else:
        result.update(dict(dest=dest, src=source, changed=changed))
    if diffs:
        result['diff'] = diffs
    return result
