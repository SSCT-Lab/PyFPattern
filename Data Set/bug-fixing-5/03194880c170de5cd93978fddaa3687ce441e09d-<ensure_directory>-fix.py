def ensure_directory(path, follow, recurse):
    b_path = to_bytes(path, errors='surrogate_or_strict')
    prev_state = get_state(b_path)
    if (follow and (prev_state == 'link')):
        b_path = os.path.realpath(b_path)
        path = to_native(b_path, errors='strict')
        prev_state = get_state(b_path)
    changed = False
    file_args = module.load_file_common_arguments(module.params)
    diff = initial_diff(path, 'directory', prev_state)
    if (prev_state == 'absent'):
        if module.check_mode:
            return {
                'changed': True,
                'diff': diff,
            }
        curpath = ''
        try:
            for dirname in path.strip('/').split('/'):
                curpath = '/'.join([curpath, dirname])
                if (not os.path.isabs(path)):
                    curpath = curpath.lstrip('/')
                b_curpath = to_bytes(curpath, errors='surrogate_or_strict')
                if (not os.path.exists(b_curpath)):
                    try:
                        os.mkdir(b_curpath)
                        changed = True
                    except OSError as ex:
                        if (not ((ex.errno == errno.EEXIST) and os.path.isdir(b_curpath))):
                            raise
                    tmp_file_args = file_args.copy()
                    tmp_file_args['path'] = curpath
                    changed = module.set_fs_attributes_if_different(tmp_file_args, changed, diff, expand=False)
        except Exception as e:
            raise AnsibleModuleError(results={
                'msg': ('There was an issue creating %s as requested: %s' % (curpath, to_native(e))),
                'path': path,
            })
    elif (prev_state != 'directory'):
        raise AnsibleModuleError(results={
            'msg': ('%s already exists as a %s' % (path, prev_state)),
            'path': path,
        })
    changed = module.set_fs_attributes_if_different(file_args, changed, diff, expand=False)
    if recurse:
        changed |= recursive_set_attributes(to_bytes(file_args['path'], errors='surrogate_or_strict'), follow, file_args)
    return {
        'path': path,
        'changed': changed,
        'diff': diff,
    }