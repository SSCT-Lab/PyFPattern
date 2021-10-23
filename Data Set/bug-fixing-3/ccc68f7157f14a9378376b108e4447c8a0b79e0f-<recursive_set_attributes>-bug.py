def recursive_set_attributes(module, b_path, follow, file_args):
    changed = False
    for (b_root, b_dirs, b_files) in os.walk(b_path):
        for b_fsobj in (b_dirs + b_files):
            b_fsname = os.path.join(b_root, b_fsobj)
            if (not os.path.islink(b_fsname)):
                tmp_file_args = file_args.copy()
                tmp_file_args['path'] = to_native(b_fsname, errors='surrogate_or_strict')
                changed |= module.set_fs_attributes_if_different(tmp_file_args, changed)
            else:
                tmp_file_args = file_args.copy()
                tmp_file_args['path'] = to_native(b_fsname, errors='surrogate_or_strict')
                changed |= module.set_fs_attributes_if_different(tmp_file_args, changed)
                if follow:
                    b_fsname = os.path.join(b_root, os.readlink(b_fsname))
                    if os.path.isdir(b_fsname):
                        changed |= recursive_set_attributes(module, b_fsname, follow, file_args)
                    tmp_file_args = file_args.copy()
                    tmp_file_args['path'] = to_native(b_fsname, errors='surrogate_or_strict')
                    changed |= module.set_fs_attributes_if_different(tmp_file_args, changed)
    return changed