def setup_extension(self, ext, package, default_include_dirs=[], default_library_dirs=[], default_libraries=[], alt_exec=None):
    '\n        Add parameters to the given `ext` for the given `package`.\n        '
    flag_map = {
        '-I': 'include_dirs',
        '-L': 'library_dirs',
        '-l': 'libraries',
    }
    executable = alt_exec
    if self.has_pkgconfig:
        executable = (self.pkg_config + ' {0}').format(package)
    use_defaults = True
    if (executable is not None):
        command = '{0} --libs --cflags '.format(executable)
        try:
            output = check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            pass
        else:
            output = output.decode(sys.getfilesystemencoding())
            use_defaults = False
            for token in output.split():
                attr = flag_map.get(token[:2])
                if (attr is not None):
                    getattr(ext, attr).insert(0, token[2:])
    if use_defaults:
        basedirs = get_base_dirs()
        for base in basedirs:
            for include in default_include_dirs:
                dir = os.path.join(base, include)
                if os.path.exists(dir):
                    ext.include_dirs.append(dir)
            for lib in default_library_dirs:
                dir = os.path.join(base, lib)
                if os.path.exists(dir):
                    ext.library_dirs.append(dir)
        ext.libraries.extend(default_libraries)
        return True
    return False