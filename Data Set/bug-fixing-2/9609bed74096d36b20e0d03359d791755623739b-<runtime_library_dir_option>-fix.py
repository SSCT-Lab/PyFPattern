

def runtime_library_dir_option(self, dir):
    if ((sys.platform[:3] == 'aix') or (sys.platform == 'win32')):
        raise NotImplementedError
    sep = (',' if (sys.platform == 'darwin') else '=')
    return ('-Wl,-rpath%s"%s"' % (sep, dir))
