

def main():
    module = AnsibleModule(argument_spec=dict(state=dict(choices=['file', 'directory', 'link', 'hard', 'touch', 'absent'], default=None), path=dict(aliases=['dest', 'name'], required=True, type='path'), original_basename=dict(required=False), recurse=dict(default=False, type='bool'), force=dict(required=False, default=False, type='bool'), follow=dict(required=False, default=True, type='bool'), diff_peek=dict(default=None), validate=dict(required=False, default=None), src=dict(required=False, default=None, type='path')), add_file_common_args=True, supports_check_mode=True)
    params = module.params
    state = params['state']
    recurse = params['recurse']
    force = params['force']
    diff_peek = params['diff_peek']
    src = params['src']
    b_src = to_bytes(src, errors='surrogate_or_strict')
    follow = params['follow']
    path = params['path']
    b_path = to_bytes(path, errors='surrogate_or_strict')
    if (diff_peek is not None):
        appears_binary = False
        try:
            f = open(b_path, 'rb')
            head = f.read(8192)
            f.close()
            if (b('\x00') in head):
                appears_binary = True
        except:
            pass
        module.exit_json(path=path, changed=False, appears_binary=appears_binary)
    prev_state = get_state(b_path)
    if (state is None):
        if (prev_state != 'absent'):
            state = prev_state
        elif recurse:
            state = 'directory'
        else:
            state = 'file'
    if (src is None):
        if (state in ('link', 'hard')):
            if (follow and (state == 'link')):
                src = to_native(os.path.realpath(b_path), errors='strict')
                b_src = to_bytes(os.path.realpath(b_path), errors='strict')
            else:
                module.fail_json(msg='src and dest are required for creating links')
    if ((state not in ('link', 'absent')) and os.path.isdir(b_path)):
        basename = None
        if params['original_basename']:
            basename = params['original_basename']
        elif (src is not None):
            basename = os.path.basename(src)
        if basename:
            params['path'] = path = os.path.join(path, basename)
            b_path = to_bytes(path, errors='surrogate_or_strict')
            prev_state = get_state(b_path)
    if (recurse and (state != 'directory')):
        module.fail_json(path=path, msg="recurse option requires state to be 'directory'")
    file_args = module.load_file_common_arguments(params)
    changed = False
    diff = {
        'before': {
            'path': path,
        },
        'after': {
            'path': path,
        },
    }
    state_change = False
    if (prev_state != state):
        diff['before']['state'] = prev_state
        diff['after']['state'] = state
        state_change = True
    if (state == 'absent'):
        if state_change:
            if (not module.check_mode):
                if (prev_state == 'directory'):
                    try:
                        shutil.rmtree(b_path, ignore_errors=False)
                    except Exception as e:
                        module.fail_json(msg=('rmtree failed: %s' % to_native(e)))
                else:
                    try:
                        os.unlink(b_path)
                    except Exception as e:
                        module.fail_json(path=path, msg=('unlinking failed: %s ' % to_native(e)))
            module.exit_json(path=path, changed=True, diff=diff)
        else:
            module.exit_json(path=path, changed=False)
    elif (state == 'file'):
        if state_change:
            if (follow and (prev_state == 'link')):
                b_path = os.path.realpath(b_path)
                path = to_native(b_path, errors='strict')
                prev_state = get_state(b_path)
                file_args['path'] = path
        if (prev_state not in ('file', 'hard')):
            module.fail_json(path=path, msg=('file (%s) is %s, cannot continue' % (path, prev_state)))
        changed = module.set_fs_attributes_if_different(file_args, changed, diff, expand=False)
        module.exit_json(path=path, changed=changed, diff=diff)
    elif (state == 'directory'):
        if (follow and (prev_state == 'link')):
            b_path = os.path.realpath(b_path)
            path = to_native(b_path, errors='strict')
            prev_state = get_state(b_path)
        if (prev_state == 'absent'):
            if module.check_mode:
                module.exit_json(changed=True, diff=diff)
            changed = True
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
                        except OSError as ex:
                            if (not ((ex.errno == errno.EEXIST) and os.path.isdir(b_curpath))):
                                raise
                        tmp_file_args = file_args.copy()
                        tmp_file_args['path'] = curpath
                        changed = module.set_fs_attributes_if_different(tmp_file_args, changed, diff, expand=False)
            except Exception as e:
                module.fail_json(path=path, msg=('There was an issue creating %s as requested: %s' % (curpath, to_native(e))))
        elif (prev_state != 'directory'):
            module.fail_json(path=path, msg=('%s already exists as a %s' % (path, prev_state)))
        changed = module.set_fs_attributes_if_different(file_args, changed, diff, expand=False)
        if recurse:
            changed |= recursive_set_attributes(module, to_bytes(file_args['path'], errors='surrogate_or_strict'), follow, file_args)
        module.exit_json(path=path, changed=changed, diff=diff)
    elif (state in ('link', 'hard')):
        if ((not os.path.islink(b_path)) and os.path.isdir(b_path)):
            relpath = path
        else:
            b_relpath = os.path.dirname(b_path)
            relpath = to_native(b_relpath, errors='strict')
        absrc = os.path.join(relpath, src)
        b_absrc = to_bytes(absrc, errors='surrogate_or_strict')
        if ((not force) and (not os.path.exists(b_absrc))):
            module.fail_json(path=path, src=src, msg=('src file does not exist, use "force=yes" if you really want to create the link: %s' % absrc))
        if (state == 'hard'):
            if (not os.path.isabs(b_src)):
                module.fail_json(msg='absolute paths are required')
        elif (prev_state == 'directory'):
            if (not force):
                module.fail_json(path=path, msg=('refusing to convert between %s and %s for %s' % (prev_state, state, path)))
            elif os.listdir(b_path):
                module.fail_json(path=path, msg=('the directory %s is not empty, refusing to convert it' % path))
        elif ((prev_state in ('file', 'hard')) and (not force)):
            module.fail_json(path=path, msg=('refusing to convert between %s and %s for %s' % (prev_state, state, path)))
        if (prev_state == 'absent'):
            changed = True
        elif (prev_state == 'link'):
            b_old_src = os.readlink(b_path)
            if (b_old_src != b_src):
                diff['before']['src'] = to_native(b_old_src, errors='strict')
                diff['after']['src'] = src
                changed = True
        elif (prev_state == 'hard'):
            if (not ((state == 'hard') and (os.stat(b_path).st_ino == os.stat(b_src).st_ino))):
                changed = True
                if (not force):
                    module.fail_json(dest=path, src=src, msg='Cannot link, different hard link exists at destination')
        elif (prev_state == 'file'):
            changed = True
            if (not force):
                module.fail_json(dest=path, src=src, msg=('Cannot link, %s exists at destination' % prev_state))
        elif (prev_state == 'directory'):
            changed = True
            if os.path.exists(b_path):
                if ((state == 'hard') and (os.stat(b_path).st_ino == os.stat(b_src).st_ino)):
                    module.exit_json(path=path, changed=False)
                elif (not force):
                    module.fail_json(dest=path, src=src, msg='Cannot link, different hard link exists at destination')
        else:
            module.fail_json(dest=path, src=src, msg='unexpected position reached')
        if (changed and (not module.check_mode)):
            if (prev_state != 'absent'):
                b_tmppath = to_bytes(os.path.sep).join([os.path.dirname(b_path), to_bytes(('.%s.%s.tmp' % (os.getpid(), time.time())))])
                try:
                    if ((prev_state == 'directory') and (state == 'link')):
                        os.rmdir(b_path)
                    elif ((prev_state == 'directory') and (state == 'hard')):
                        if os.path.exists(b_path):
                            os.remove(b_path)
                    if (state == 'hard'):
                        os.link(b_src, b_tmppath)
                    else:
                        os.symlink(b_src, b_tmppath)
                    os.rename(b_tmppath, b_path)
                except OSError as e:
                    if os.path.exists(b_tmppath):
                        os.unlink(b_tmppath)
                    module.fail_json(path=path, msg=('Error while replacing: %s' % to_native(e, nonstring='simplerepr')))
            else:
                try:
                    if (state == 'hard'):
                        os.link(b_src, b_path)
                    else:
                        os.symlink(b_src, b_path)
                except OSError as e:
                    module.fail_json(path=path, msg=('Error while linking: %s' % to_native(e, nonstring='simplerepr')))
        if (module.check_mode and (not os.path.exists(b_path))):
            module.exit_json(dest=path, src=src, changed=changed, diff=diff)
        changed = module.set_fs_attributes_if_different(file_args, changed, diff, expand=False)
        module.exit_json(dest=path, src=src, changed=changed, diff=diff)
    elif (state == 'touch'):
        if (not module.check_mode):
            if (prev_state == 'absent'):
                try:
                    open(b_path, 'wb').close()
                except (OSError, IOError) as e:
                    module.fail_json(path=path, msg=('Error, could not touch target: %s' % to_native(e, nonstring='simplerepr')))
            elif (prev_state in ('file', 'directory', 'hard')):
                try:
                    os.utime(b_path, None)
                except OSError as e:
                    module.fail_json(path=path, msg=('Error while touching existing target: %s' % to_native(e, nonstring='simplerepr')))
            else:
                module.fail_json(msg=('Cannot touch other than files, directories, and hardlinks (%s is %s)' % (path, prev_state)))
            try:
                module.set_fs_attributes_if_different(file_args, True, diff, expand=False)
            except SystemExit as e:
                if e.code:
                    if (prev_state == 'absent'):
                        os.remove(b_path)
                raise e
        module.exit_json(dest=path, changed=True, diff=diff)
    module.fail_json(path=path, msg='unexpected position reached')
