

def run(self, tmp=None, task_vars=None):
    ' handler for file transfer operations '
    if (task_vars is None):
        task_vars = dict()
    result = super(ActionModule, self).run(tmp, task_vars)
    del tmp
    source = self._task.args.get('src', None)
    content = self._task.args.get('content', None)
    dest = self._task.args.get('dest', None)
    remote_src = boolean(self._task.args.get('remote_src', False), strict=False)
    local_follow = boolean(self._task.args.get('local_follow', True), strict=False)
    result['failed'] = True
    if ((not source) and (content is None)):
        result['msg'] = 'src (or content) is required'
    elif (not dest):
        result['msg'] = 'dest is required'
    elif (source and (content is not None)):
        result['msg'] = 'src and content are mutually exclusive'
    elif ((content is not None) and (dest is not None) and dest.endswith('/')):
        result['msg'] = 'can not use content with a dir as dest'
    else:
        del result['failed']
    if result.get('failed'):
        return result
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
    elif remote_src:
        result.update(self._execute_module(task_vars=task_vars))
        return result
    else:
        trailing_slash = source.endswith(os.path.sep)
        try:
            source = self._find_needle('files', source)
        except AnsibleError as e:
            result['failed'] = True
            result['msg'] = to_text(e)
            result['exception'] = traceback.format_exc()
            return result
        if (trailing_slash != source.endswith(os.path.sep)):
            if (source[(- 1)] == os.path.sep):
                source = source[:(- 1)]
            else:
                source = (source + os.path.sep)
    source_files = {
        'files': [],
        'directories': [],
        'symlinks': [],
    }
    if os.path.isdir(to_bytes(source, errors='surrogate_or_strict')):
        source_files = _walk_dirs(source, local_follow=local_follow, trailing_slash_detector=self._connection._shell.path_has_trailing_slash)
        if (not self._connection._shell.path_has_trailing_slash(dest)):
            dest = self._connection._shell.join_path(dest, '')
    else:
        source_files['files'] = [(source, os.path.basename(source))]
    changed = False
    module_return = dict(changed=False)
    module_executed = False
    dest = self._remote_expand_user(dest)
    implicit_directories = set()
    for (source_full, source_rel) in source_files['files']:
        module_return = self._copy_file(source_full, source_rel, content, content_tempfile, dest, task_vars)
        if (module_return is None):
            continue
        paths = os.path.split(source_rel)
        dir_path = ''
        for dir_component in paths:
            os.path.join(dir_path, dir_component)
            implicit_directories.add(dir_path)
        if (('diff' in result) and (not result['diff'])):
            del result['diff']
        module_executed = True
        changed = (changed or module_return.get('changed', False))
    for (src, dest_path) in source_files['directories']:
        if (dest_path in implicit_directories):
            continue
        new_module_args = self._get_file_args()
        new_module_args['path'] = os.path.join(dest, dest_path)
        new_module_args['state'] = 'directory'
        new_module_args['mode'] = self._task.args.get('directory_mode', None)
        module_return = self._execute_module(module_name='file', module_args=new_module_args, task_vars=task_vars)
        module_executed = True
        changed = (changed or module_return.get('changed', False))
    for (target_path, dest_path) in source_files['symlinks']:
        new_module_args = self._get_file_args()
        new_module_args['path'] = os.path.join(dest, dest_path)
        new_module_args['src'] = target_path
        new_module_args['state'] = 'link'
        new_module_args['force'] = True
        module_return = self._execute_module(module_name='file', module_args=new_module_args, task_vars=task_vars)
        module_executed = True
        if module_return.get('failed'):
            result.update(module_return)
            return result
        changed = (changed or module_return.get('changed', False))
    if (module_executed and (len(source_files['files']) == 1)):
        result.update(module_return)
        if (('path' in result) and ('dest' not in result)):
            result['dest'] = result['path']
    else:
        result.update(dict(dest=dest, src=source, changed=changed))
    self._remove_tmp_path(self._connection._shell.tmpdir)
    return result
