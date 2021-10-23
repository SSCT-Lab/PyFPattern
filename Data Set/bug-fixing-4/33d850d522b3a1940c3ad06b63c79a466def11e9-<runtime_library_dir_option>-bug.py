def runtime_library_dir_option(self, dir):
    return ('-Wl,-rpath="%s"' % dir)