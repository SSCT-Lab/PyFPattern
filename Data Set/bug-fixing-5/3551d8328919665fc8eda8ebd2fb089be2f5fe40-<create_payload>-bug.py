def create_payload(args, dst_path):
    'Create a payload for delegation.'
    if args.explain:
        return
    files = list(data_context().ansible_source)
    if (not ANSIBLE_SOURCE_ROOT):
        files.extend(create_temporary_bin_files(args))
    if (not data_context().content.is_ansible):
        files = [f for f in files if (is_subdir(f[1], 'bin/') or is_subdir(f[1], 'lib/ansible/') or (is_subdir(f[1], 'test/lib/ansible_test/') and (not is_subdir(f[1], 'test/lib/ansible_test/tests/'))))]
        if (not isinstance(args, (ShellConfig, IntegrationConfig))):
            files = [f for f in files if ((not is_subdir(f[1], 'lib/ansible/modules/')) or (f[1] == 'lib/ansible/modules/__init__.py'))]
        if data_context().content.collection:
            files.extend(((os.path.join(data_context().content.root, path), os.path.join(data_context().content.collection.directory, path)) for path in data_context().content.all_files()))
    for callback in data_context().payload_callbacks:
        callback(files)
    files = sorted(set(files))
    display.info(('Creating a payload archive containing %d files...' % len(files)), verbosity=1)
    start = time.time()
    with tarfile.TarFile.gzopen(dst_path, mode='w', compresslevel=4) as tar:
        for (src, dst) in files:
            display.info(('%s -> %s' % (src, dst)), verbosity=4)
            tar.add(src, dst)
    duration = (time.time() - start)
    payload_size_bytes = os.path.getsize(dst_path)
    display.info(('Created a %d byte payload archive containing %d files in %d seconds.' % (payload_size_bytes, len(files), duration)), verbosity=1)