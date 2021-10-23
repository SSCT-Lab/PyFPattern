def ensure_file_attributes(path, prev_state, follow):
    b_path = to_bytes(path, errors='surrogate_or_strict')
    file_args = module.load_file_common_arguments(module.params)
    if (prev_state != 'file'):
        if (follow and (prev_state == 'link')):
            b_path = os.path.realpath(b_path)
            path = to_native(b_path, errors='strict')
            prev_state = get_state(b_path)
            file_args['path'] = path
    if (prev_state not in ('file', 'hard')):
        raise AnsibleModuleError(results={
            'msg': ('file (%s) is %s, cannot continue' % (path, prev_state)),
            'path': path,
        })
    diff = initial_diff(path, 'file', prev_state)
    changed = module.set_fs_attributes_if_different(file_args, False, diff, expand=False)
    return {
        'path': path,
        'changed': changed,
        'diff': diff,
    }