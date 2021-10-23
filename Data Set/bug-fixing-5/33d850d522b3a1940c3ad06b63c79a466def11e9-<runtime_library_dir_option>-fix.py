def runtime_library_dir_option(self, dir):
    sep = (',' if (sys.platform == 'darwin') else '=')
    return ('-Wl,-rpath%s"%s"' % (sep, dir))