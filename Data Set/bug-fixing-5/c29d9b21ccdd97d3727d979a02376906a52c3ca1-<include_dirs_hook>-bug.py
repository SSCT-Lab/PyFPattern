@staticmethod
def include_dirs_hook():
    import builtins
    if hasattr(builtins, '__NUMPY_SETUP__'):
        del builtins.__NUMPY_SETUP__
    import imp
    import numpy
    imp.reload(numpy)
    ext = Extension('test', [])
    ext.include_dirs.append(numpy.get_include())
    if (not has_include_file(ext.include_dirs, os.path.join('numpy', 'arrayobject.h'))):
        warnings.warn('The C headers for numpy could not be found. You may need to install the development package')
    return [numpy.get_include()]