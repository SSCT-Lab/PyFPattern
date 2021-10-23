def adjust_recursive_directory_permissions(pre_existing_dir, new_directory_list, module, directory_args, changed):
    '\n    Walk the new directories list and make sure that permissions are as we would expect\n    '
    if (len(new_directory_list) > 0):
        working_dir = os.path.join(pre_existing_dir, new_directory_list.pop(0))
        directory_args['path'] = working_dir
        changed = module.set_fs_attributes_if_different(directory_args, changed)
        changed = adjust_recursive_directory_permissions(working_dir, new_directory_list, module, directory_args, changed)
    return changed