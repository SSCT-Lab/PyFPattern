def _maintain_symlinks(symlink_type, base_path):
    'Switch a real file into a symlink'
    try:
        with open(SYMLINK_CACHE, 'r') as f:
            symlink_data = json.loads(f.read())
    except IOError as e:
        if (e.errno == 2):
            symlink_data = {
                'script': _find_symlinks('bin'),
                'library': _find_symlinks('lib', '.py'),
            }
            if ('ansible-playbook' in symlink_data['script']['ansible']):
                _cache_symlinks(symlink_data)
            else:
                raise
        else:
            raise
    symlinks = symlink_data[symlink_type]
    for source in symlinks:
        for dest in symlinks[source]:
            dest_path = os.path.join(base_path, dest)
            if (not os.path.islink(dest_path)):
                try:
                    os.unlink(dest_path)
                except OSError as e:
                    if (e.errno == 2):
                        pass
                os.symlink(source, dest_path)