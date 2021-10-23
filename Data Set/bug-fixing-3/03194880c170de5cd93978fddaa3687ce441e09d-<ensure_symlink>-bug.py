def ensure_symlink(path, src, b_src, prev_state, follow, force):
    b_path = to_bytes(path, errors='surrogate_or_strict')
    file_args = module.load_file_common_arguments(module.params)
    if (src is None):
        if follow:
            src = to_native(os.path.realpath(b_path), errors='strict')
            b_src = to_bytes(os.path.realpath(b_path), errors='strict')
    if ((not os.path.islink(b_path)) and os.path.isdir(b_path)):
        relpath = path
    else:
        b_relpath = os.path.dirname(b_path)
        relpath = to_native(b_relpath, errors='strict')
    absrc = os.path.join(relpath, src)
    b_absrc = to_bytes(absrc, errors='surrogate_or_strict')
    if ((not force) and (not os.path.exists(b_absrc))):
        raise AnsibleModuleError(results={
            'msg': ('src file does not exist, use "force=yes" if you really want to create the link: %s' % absrc),
            'path': path,
            'src': src,
        })
    if (prev_state == 'directory'):
        if (not force):
            raise AnsibleModuleError(results={
                'msg': ('refusing to convert from %s to symlink for %s' % (prev_state, path)),
                'path': path,
            })
        elif os.listdir(b_path):
            raise AnsibleModuleError(results={
                'msg': ('the directory %s is not empty, refusing to convert it' % path),
                'path': path,
            })
    elif ((prev_state in ('file', 'hard')) and (not force)):
        raise AnsibleModuleError(results={
            'msg': ('refusing to convert from %s to symlink for %s' % (prev_state, path)),
            'path': path,
        })
    diff = initial_diff(path, 'link', prev_state)
    changed = False
    if (prev_state == 'absent'):
        changed = True
    elif (prev_state == 'link'):
        b_old_src = os.readlink(b_path)
        if (b_old_src != b_src):
            diff['before']['src'] = to_native(b_old_src, errors='strict')
            diff['after']['src'] = src
            changed = True
    elif (prev_state == 'hard'):
        changed = True
        if (not force):
            raise AnsibleModuleError(results={
                'msg': 'Cannot link, different hard link exists at destination',
                'dest': path,
                'src': src,
            })
    elif (prev_state == 'file'):
        changed = True
        if (not force):
            raise AnsibleModuleError(results={
                'msg': ('Cannot link, %s exists at destination' % prev_state),
                'dest': path,
                'src': src,
            })
    elif (prev_state == 'directory'):
        changed = True
        if os.path.exists(b_path):
            if (not force):
                raise AnsibleModuleError(results={
                    'msg': 'Cannot link, different hard link exists at destination',
                    'dest': path,
                    'src': src,
                })
    else:
        raise AnsibleModuleError(results={
            'msg': 'unexpected position reached',
            'dest': path,
            'src': src,
        })
    if (changed and (not module.check_mode)):
        if (prev_state != 'absent'):
            b_tmppath = to_bytes(os.path.sep).join([os.path.dirname(b_path), to_bytes(('.%s.%s.tmp' % (os.getpid(), time.time())))])
            try:
                if (prev_state == 'directory'):
                    os.rmdir(b_path)
                os.symlink(b_src, b_tmppath)
                os.rename(b_tmppath, b_path)
            except OSError as e:
                if os.path.exists(b_tmppath):
                    os.unlink(b_tmppath)
                raise AnsibleModuleError(results={
                    'msg': ('Error while replacing: %s' % to_native(e, nonstring='simplerepr')),
                    'path': path,
                })
        else:
            try:
                os.symlink(b_src, b_path)
            except OSError as e:
                raise AnsibleModuleError(results={
                    'msg': ('Error while linking: %s' % to_native(e, nonstring='simplerepr')),
                    'path': path,
                })
    if (module.check_mode and (not os.path.exists(b_path))):
        return {
            'dest': path,
            'src': src,
            'changed': changed,
            'diff': diff,
        }
    if (follow and os.path.islink(b_path) and (not os.path.exists(file_args['path']))):
        module.warn('Cannot set fs attributes on a non-existent symlink target. follow should be set to False to avoid this.')
    else:
        changed = module.set_fs_attributes_if_different(file_args, changed, diff, expand=False)
    return {
        'dest': path,
        'src': src,
        'changed': changed,
        'diff': diff,
    }