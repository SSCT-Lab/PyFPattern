def execute_touch(path, follow):
    b_path = to_bytes(path, errors='surrogate_or_strict')
    prev_state = get_state(b_path)
    if (not module.check_mode):
        if (prev_state == 'absent'):
            try:
                open(b_path, 'wb').close()
            except (OSError, IOError) as e:
                raise AnsibleModuleError(results={
                    'msg': ('Error, could not touch target: %s' % to_native(e, nonstring='simplerepr')),
                    'path': path,
                })
        elif (prev_state in ('file', 'directory', 'hard')):
            try:
                os.utime(b_path, None)
            except OSError as e:
                raise AnsibleModuleError(results={
                    'msg': ('Error while touching existing target: %s' % to_native(e, nonstring='simplerepr')),
                    'path': path,
                })
        elif ((prev_state == 'link') and follow):
            b_link_target = os.readlink(b_path)
            try:
                os.utime(b_link_target, None)
            except OSError as e:
                raise AnsibleModuleError(results={
                    'msg': ('Error while touching existing target: %s' % to_native(e, nonstring='simplerepr')),
                    'path': path,
                })
        else:
            raise AnsibleModuleError(results={
                'msg': ('Can only touch files, directories, and hardlinks (%s is %s)' % (path, prev_state)),
            })
        diff = initial_diff(path, 'absent', prev_state)
        file_args = module.load_file_common_arguments(module.params)
        try:
            module.set_fs_attributes_if_different(file_args, True, diff, expand=False)
        except SystemExit as e:
            if e.code:
                if (prev_state == 'absent'):
                    os.remove(b_path)
            raise
    return {
        'dest': path,
        'changed': True,
    }