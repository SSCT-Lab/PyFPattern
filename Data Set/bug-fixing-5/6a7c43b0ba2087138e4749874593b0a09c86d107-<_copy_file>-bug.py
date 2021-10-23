def _copy_file(self, source_full, source_rel, content, content_tempfile, dest, task_vars, follow):
    decrypt = boolean(self._task.args.get('decrypt', True), strict=False)
    force = boolean(self._task.args.get('force', 'yes'), strict=False)
    raw = boolean(self._task.args.get('raw', 'no'), strict=False)
    result = {
        
    }
    result['diff'] = []
    try:
        source_full = self._loader.get_real_file(source_full, decrypt=decrypt)
    except AnsibleFileNotFound as e:
        result['failed'] = True
        result['msg'] = ('could not find src=%s, %s' % (source_full, to_text(e)))
        return result
    lmode = None
    if (self._task.args.get('mode', None) == 'preserve'):
        lmode = ('0%03o' % stat.S_IMODE(os.stat(source_full).st_mode))
    if self._connection._shell.path_has_trailing_slash(dest):
        dest_file = self._connection._shell.join_path(dest, source_rel)
    else:
        dest_file = dest
    dest_status = self._execute_remote_stat(dest_file, all_vars=task_vars, follow=follow, checksum=force)
    if (dest_status['exists'] and dest_status['isdir']):
        if (content is not None):
            self._remove_tempfile_if_content_defined(content, content_tempfile)
            result['failed'] = True
            result['msg'] = 'can not use content with a dir as dest'
            return result
        else:
            dest_file = self._connection._shell.join_path(dest, source_rel)
            dest_status = self._execute_remote_stat(dest_file, all_vars=task_vars, follow=follow, checksum=force)
    if (dest_status['exists'] and (not force)):
        return None
    local_checksum = checksum(source_full)
    if (local_checksum != dest_status['checksum']):
        if (self._play_context.diff and (not raw)):
            result['diff'].append(self._get_diff_data(dest_file, source_full, task_vars))
        if self._play_context.check_mode:
            self._remove_tempfile_if_content_defined(content, content_tempfile)
            result['changed'] = True
            return result
        tmp_src = self._connection._shell.join_path(self._connection._shell.tmpdir, 'source')
        remote_path = None
        if (not raw):
            remote_path = self._transfer_file(source_full, tmp_src)
        else:
            self._transfer_file(source_full, dest_file)
        self._remove_tempfile_if_content_defined(content, content_tempfile)
        self._loader.cleanup_tmp_file(source_full)
        if remote_path:
            self._fixup_perms2((self._connection._shell.tmpdir, remote_path))
        if raw:
            return None
        new_module_args = self._create_remote_file_args(self._task.args)
        new_module_args.update(dict(src=tmp_src, dest=dest, original_basename=source_rel, follow=follow))
        if (not self._task.args.get('checksum')):
            new_module_args['checksum'] = local_checksum
        if lmode:
            new_module_args['mode'] = lmode
        module_return = self._execute_module(module_name='copy', module_args=new_module_args, task_vars=task_vars)
    else:
        self._remove_tempfile_if_content_defined(content, content_tempfile)
        self._loader.cleanup_tmp_file(source_full)
        if raw:
            return None
        if follow:
            dest_status_nofollow = self._execute_remote_stat(dest_file, all_vars=task_vars, follow=False)
            if (dest_status_nofollow['islnk'] and ('lnk_source' in dest_status_nofollow.keys())):
                dest = dest_status_nofollow['lnk_source']
        new_module_args = self._create_remote_file_args(self._task.args)
        new_module_args.update(dict(src=source_rel, dest=dest, original_basename=source_rel, state='file'))
        if lmode:
            new_module_args['mode'] = lmode
        module_return = self._execute_module(module_name='file', module_args=new_module_args, task_vars=task_vars)
    if (not module_return.get('checksum')):
        module_return['checksum'] = local_checksum
    result.update(module_return)
    return result