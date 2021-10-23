def main():
    global module
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['file', 'directory', 'link', 'hard', 'touch', 'absent'], default=None), path=dict(aliases=['dest', 'name'], required=True, type='path'), original_basename=dict(required=False), recurse=dict(default=False, type='bool'), force=dict(required=False, default=False, type='bool'), follow=dict(required=False, default=True, type='bool'), _diff_peek=dict(default=None), src=dict(required=False, default=None, type='path')), add_file_common_args=True, supports_check_mode=True)
    sys.excepthook = _ansible_excepthook
    additional_parameter_handling(module.params)
    params = module.params
    state = params['state']
    recurse = params['recurse']
    force = params['force']
    follow = params['follow']
    path = params['path']
    b_path = params['b_path']
    src = params['src']
    b_src = params['b_src']
    prev_state = get_state(b_path)
    if (params['_diff_peek'] is not None):
        appears_binary = execute_diff_peek(b_path)
        module.exit_json(path=path, changed=False, appears_binary=appears_binary)
    if ((state not in ('link', 'absent')) and os.path.isdir(b_path)):
        basename = None
        if params['original_basename']:
            basename = params['original_basename']
        elif (b_src is not None):
            basename = os.path.basename(b_src)
        if basename:
            params['path'] = path = os.path.join(path, basename)
            b_path = to_bytes(path, errors='surrogate_or_strict')
            prev_state = get_state(b_path)
    if (state == 'file'):
        result = ensure_file_attributes(path, b_path, prev_state, follow)
    elif (state == 'directory'):
        result = ensure_directory(path, b_path, prev_state, follow, recurse)
    elif (state == 'link'):
        result = ensure_symlink(path, b_path, src, b_src, prev_state, follow, force)
    elif (state == 'hard'):
        result = ensure_hardlink(path, b_path, src, b_src, prev_state, follow, force)
    elif (state == 'touch'):
        result = execute_touch(path, b_path, prev_state, follow)
    elif (state == 'absent'):
        result = ensure_absent(path, b_path, prev_state)
        module.exit_json(**result)
    module.exit_json(**result)