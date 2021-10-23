def ensure_absent(path, prev_state):
    b_path = to_bytes(path, errors='surrogate_or_strict')
    result = {
        
    }
    if (prev_state != 'absent'):
        if (not module.check_mode):
            if (prev_state == 'directory'):
                try:
                    shutil.rmtree(b_path, ignore_errors=False)
                except Exception as e:
                    raise AnsibleModuleError(results={
                        'msg': ('rmtree failed: %s' % to_native(e)),
                    })
            else:
                try:
                    os.unlink(b_path)
                except OSError as e:
                    if (e.errno != errno.ENOENT):
                        raise AnsibleModuleError(results={
                            'msg': ('unlinking failed: %s ' % to_native(e)),
                            'path': path,
                        })
        diff = initial_diff(path, 'absent', prev_state)
        result.update({
            'path': path,
            'changed': True,
            'diff': diff,
        })
    else:
        result.update({
            'path': path,
            'changed': False,
        })
    return result