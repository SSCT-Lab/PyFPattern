

def main():
    module = AnsibleModule(argument_spec=dict(src=dict(required=False, type='path'), original_basename=dict(required=False), content=dict(required=False, no_log=True), dest=dict(required=True, type='path'), backup=dict(default=False, type='bool'), force=dict(default=True, aliases=['thirsty'], type='bool'), validate=dict(required=False, type='str'), directory_mode=dict(required=False, type='raw'), remote_src=dict(required=False, type='bool')), add_file_common_args=True, supports_check_mode=True)
    src = module.params['src']
    b_src = to_bytes(src, errors='surrogate_or_strict')
    dest = module.params['dest']
    b_dest = to_bytes(dest, errors='surrogate_or_strict')
    backup = module.params['backup']
    force = module.params['force']
    original_basename = module.params.get('original_basename', None)
    validate = module.params.get('validate', None)
    follow = module.params['follow']
    mode = module.params['mode']
    remote_src = module.params['remote_src']
    if (not os.path.exists(b_src)):
        module.fail_json(msg=('Source %s not found' % src))
    if (not os.access(b_src, os.R_OK)):
        module.fail_json(msg=('Source %s not readable' % src))
    if os.path.isdir(b_src):
        module.fail_json(msg=('Remote copy does not support recursive copy of directory: %s' % src))
    checksum_src = module.sha1(src)
    checksum_dest = None
    try:
        md5sum_src = module.md5(src)
    except ValueError:
        md5sum_src = None
    changed = False
    if (original_basename and dest.endswith(os.sep)):
        dest = os.path.join(dest, original_basename)
        b_dest = to_bytes(dest, errors='surrogate_or_strict')
        dirname = os.path.dirname(dest)
        b_dirname = to_bytes(dirname, errors='surrogate_or_strict')
        if ((not os.path.exists(b_dirname)) and os.path.isabs(b_dirname)):
            (pre_existing_dir, new_directory_list) = split_pre_existing_dir(dirname)
            os.makedirs(b_dirname)
            directory_args = module.load_file_common_arguments(module.params)
            directory_mode = module.params['directory_mode']
            if (directory_mode is not None):
                directory_args['mode'] = directory_mode
            else:
                directory_args['mode'] = None
            adjust_recursive_directory_permissions(pre_existing_dir, new_directory_list, module, directory_args, changed)
    if os.path.isdir(b_dest):
        basename = os.path.basename(src)
        if original_basename:
            basename = original_basename
        dest = os.path.join(dest, basename)
        b_dest = to_bytes(dest, errors='surrogate_or_strict')
    if os.path.exists(b_dest):
        if (os.path.islink(b_dest) and follow):
            b_dest = os.path.realpath(b_dest)
            dest = to_native(b_dest, errors='surrogate_or_strict')
        if (not force):
            module.exit_json(msg='file already exists', src=src, dest=dest, changed=False)
        if os.access(b_dest, os.R_OK):
            checksum_dest = module.sha1(dest)
    elif (not os.path.exists(os.path.dirname(b_dest))):
        try:
            os.stat(os.path.dirname(b_dest))
        except OSError:
            e = get_exception()
            if ('permission denied' in to_native(e).lower()):
                module.fail_json(msg=('Destination directory %s is not accessible' % os.path.dirname(dest)))
        module.fail_json(msg=('Destination directory %s does not exist' % os.path.dirname(dest)))
    if (not os.access(os.path.dirname(b_dest), os.W_OK)):
        module.fail_json(msg=('Destination %s not writable' % os.path.dirname(dest)))
    backup_file = None
    if ((checksum_src != checksum_dest) or os.path.islink(b_dest)):
        if (not module.check_mode):
            try:
                if backup:
                    if os.path.exists(b_dest):
                        backup_file = module.backup_local(dest)
                if os.path.islink(b_dest):
                    os.unlink(b_dest)
                    open(b_dest, 'w').close()
                if validate:
                    if (mode is not None):
                        module.set_mode_if_different(src, mode, False)
                    if ('%s' not in validate):
                        module.fail_json(msg=('validate must contain %%s: %s' % validate))
                    (rc, out, err) = module.run_command((validate % src))
                    if (rc != 0):
                        module.fail_json(msg='failed to validate', exit_status=rc, stdout=out, stderr=err)
                b_mysrc = b_src
                if remote_src:
                    (_, b_mysrc) = tempfile.mkstemp(dir=os.path.dirname(b_dest))
                    shutil.copy2(b_src, b_mysrc)
                module.atomic_move(b_mysrc, dest, unsafe_writes=module.params['unsafe_writes'])
            except IOError:
                module.fail_json(msg=('failed to copy: %s to %s' % (src, dest)), traceback=traceback.format_exc())
        changed = True
    else:
        changed = False
    res_args = dict(dest=dest, src=src, md5sum=md5sum_src, checksum=checksum_src, changed=changed)
    if backup_file:
        res_args['backup_file'] = backup_file
    module.params['dest'] = dest
    if (not module.check_mode):
        file_args = module.load_file_common_arguments(module.params)
        res_args['changed'] = module.set_fs_attributes_if_different(file_args, res_args['changed'])
    module.exit_json(**res_args)
