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
            result['msg'] = ('could not write content temp file: %s' % to_native(err))
            return result
    elif faf:
        source = self._get_first_available_file(faf, task_vars.get('_original_file', None))
    elif remote_src:
        result.update(self._execute_module(module_name='copy', module_args=self._task.args, task_vars=task_vars, delete_remote_tmp=False))
        return result
    else:
        try:
            source = self._find_needle('files', source)
        except AnsibleError as e:
            result['failed'] = True
            result['msg'] = to_text(e)
            return result
    source_files = []
    if os.path.isdir(to_bytes(source, errors='surrogate_or_strict')):
        if source_trailing_slash:
            sz = len(source)
        else:
            sz = (len(source.rsplit('/', 1)[0]) + 1)
        for (base_path, sub_folders, files) in os.walk(to_bytes(source)):
            for file in files:
                full_path = to_text(os.path.join(base_path, file), errors='surrogate_or_strict')
                rel_path = full_path[sz:]
                if rel_path.startswith('/'):
                    rel_path = rel_path[1:]
                source_files.append((full_path, rel_path))
            for sf in sub_folders:
                source_files += self._get_recursive_files(os.path.join(source, to_text(sf)), sz=sz)
        if (not self._connection._shell.path_has_trailing_slash(dest)):
            dest = self._connection._shell.join_path(dest, '')
    else:
        source_files.append((source, os.path.basename(source)))
    changed = False
    module_return = dict(changed=False)
    module_executed = False
    delete_remote_tmp = (len(source_files) == 1)
    remote_user = (task_vars.get('ansible_ssh_user') or self._play_context.remote_user)
    if (not delete_remote_tmp):
        if ((tmp is None) or ('-tmp-' not in tmp)):
            tmp = self._make_tmp_path(remote_user)
            self._cleanup_remote_tmp = True
    dest = self._remote_expand_user(dest)
    diffs = []
    for (source_full, source_rel) in source_files:
        source_full = self._loader.get_real_file(source_full)
        local_checksum = checksum(source_full)
        if (local_checksum is None):
            result['failed'] = True
            result['msg'] = ('could not find src=%s' % source_full)
            self._remove_tmp_path(tmp)
            return result
        if self._connection._shell.path_has_trailing_slash(dest):
            dest_file = self._connection._shell.join_path(dest, source_rel)
        else:
            dest_file = self._connection._shell.join_path(dest)
        dest_status = self._execute_remote_stat(dest_file, all_vars=task_vars, follow=follow, tmp=tmp)
        if (dest_status['exists'] and dest_status['isdir']):
            if (content is not None):
                self._remove_tempfile_if_content_defined(content, content_tempfile)
                self._remove_tmp_path(tmp)
                result['failed'] = True
                result['msg'] = 'can not use content with a dir as dest'
                return result
            else:
                dest_file = self._connection._shell.join_path(dest, source_rel)
                dest_status = self._execute_remote_stat(dest_file, all_vars=task_vars, follow=follow, tmp=tmp)
        if (dest_status['exists'] and (not force)):
            continue
        if (local_checksum != dest_status['checksum']):
            changed = True
            if delete_remote_tmp:
                if ((tmp is None) or ('-tmp-' not in tmp)):
                    tmp = self._make_tmp_path(remote_user)
                    self._cleanup_remote_tmp = True
            if (self._play_context.diff and (not raw)):
                diffs.append(self._get_diff_data(dest_file, source_full, task_vars))
            if self._play_context.check_mode:
                self._remove_tempfile_if_content_defined(content, content_tempfile)
                changed = True
                module_return = dict(changed=True)
                continue
            tmp_src = self._connection._shell.join_path(tmp, 'source')
            remote_path = None
            if (not raw):
                remote_path = self._transfer_file(source_full, tmp_src)
            else:
                self._transfer_file(source_full, dest_file)
            self._remove_tempfile_if_content_defined(content, content_tempfile)
            self._loader.cleanup_tmp_file(source_full)
            if remote_path:
                self._fixup_perms2((tmp, remote_path), remote_user)
            if raw:
                continue
            new_module_args = self._task.args.copy()
            new_module_args.update(dict(src=tmp_src, dest=dest, original_basename=source_rel))
            if ('content' in new_module_args):
                del new_module_args['content']
            module_return = self._execute_module(module_name='copy', module_args=new_module_args, task_vars=task_vars, tmp=tmp, delete_remote_tmp=delete_remote_tmp)
            module_executed = True
        else:
            self._remove_tempfile_if_content_defined(content, content_tempfile)
            self._loader.cleanup_tmp_file(source_full)
            if raw:
                self._remove_tmp_path(tmp)
                continue
            new_module_args = self._task.args.copy()
            new_module_args.update(dict(src=source_rel, dest=dest, original_basename=source_rel))
            module_return = self._execute_module(module_name='file', module_args=new_module_args, task_vars=task_vars, tmp=tmp, delete_remote_tmp=delete_remote_tmp)
            module_executed = True
        if (not module_return.get('checksum')):
            module_return['checksum'] = local_checksum
        if module_return.get('failed'):
            result.update(module_return)
            if (not delete_remote_tmp):
                self._remove_tmp_path(tmp)
            return result
        if module_return.get('changed'):
            changed = True
        if (('path' in module_return) and ('dest' not in module_return)):
            module_return['dest'] = module_return['path']
    if ((not delete_remote_tmp) or (delete_remote_tmp and (not module_executed))):
        self._remove_tmp_path(tmp)
    if (module_executed and (len(source_files) == 1)):
        result.update(module_return)
    else:
        result.update(dict(dest=dest, src=source, changed=changed))
    if diffs:
        result['diff'] = diffs
    return result