

def config_cython():
    'Try to configure cython and return cython configuration'
    if (not with_cython):
        return []
    if (os.name == 'nt'):
        print('WARNING: Cython is not supported on Windows, will compile without cython module')
        return []
    try:
        from Cython.Build import cythonize
        if (sys.version_info >= (3, 0)):
            subdir = '_cy3'
        else:
            subdir = '_cy2'
        ret = []
        path = 'mxnet/cython'
        if (os.name == 'nt'):
            library_dirs = ['mxnet', '../build/Release', '../build']
            libraries = ['libmxnet']
        else:
            library_dirs = None
            libraries = None
        for fn in os.listdir(path):
            if (not fn.endswith('.pyx')):
                continue
            ret.append(Extension(('mxnet/%s/.%s' % (subdir, fn[:(- 4)])), [('mxnet/cython/%s' % fn)], include_dirs=['../include/', '../3rdparty/nnvm/include'], library_dirs=library_dirs, libraries=libraries, language='c++'))
        return cythonize(ret)
    except ImportError:
        print('WARNING: Cython is not installed, will compile without cython module')
        return []
