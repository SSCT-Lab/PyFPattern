def create_temporary_bin_files(args):
    'Create a temporary ansible bin directory populated using the symlink map.'
    if args.explain:
        temp_path = '/tmp/ansible-tmp-bin'
    else:
        temp_path = tempfile.mkdtemp(prefix='ansible', suffix='bin')
        atexit.register(remove_tree, temp_path)
        for (name, dest) in ANSIBLE_BIN_SYMLINK_MAP.items():
            path = os.path.join(temp_path, name)
            os.link(dest, path)
    return tuple(((os.path.join(temp_path, name), os.path.join('bin', name)) for name in sorted(ANSIBLE_BIN_SYMLINK_MAP)))