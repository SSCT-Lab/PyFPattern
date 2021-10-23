def split_pre_existing_dir(dirname):
    '\n    Return the first pre-existing directory and a list of the new directories that will be created.\n    '
    (head, tail) = os.path.split(dirname)
    b_head = to_bytes(head, errors='surrogate_or_strict')
    if (not os.path.exists(b_head)):
        if (head == dirname):
            return (None, [head])
        else:
            (pre_existing_dir, new_directory_list) = split_pre_existing_dir(head)
    else:
        return (head, [tail])
    new_directory_list.append(tail)
    return (pre_existing_dir, new_directory_list)