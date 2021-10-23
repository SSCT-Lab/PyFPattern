def _find_lib(self, lib_dir, lib, exts):
    assert is_string(lib_dir)
    if (sys.platform == 'win32'):
        lib_prefixes = ['', 'lib']
    else:
        lib_prefixes = ['lib']
    for ext in exts:
        for prefix in lib_prefixes:
            p = self.combine_paths(lib_dir, ((prefix + lib) + ext))
            if p:
                break
        if p:
            assert (len(p) == 1)
            if (ext == '.dll.a'):
                lib += '.dll'
            return lib
    return False