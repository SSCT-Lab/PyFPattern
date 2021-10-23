

def process_pyx(fromfile, tofile):
    try:
        from Cython.Compiler.Version import version as cython_version
        from distutils.version import LooseVersion
        if (LooseVersion(cython_version) < LooseVersion('0.19')):
            raise Exception(('Building %s requires Cython >= 0.19' % VENDOR))
    except ImportError:
        pass
    flags = ['--fast-fail']
    if tofile.endswith('.cxx'):
        flags += ['--cplus']
    try:
        try:
            r = subprocess.call(((['cython'] + flags) + ['-o', tofile, fromfile]))
            if (r != 0):
                raise Exception('Cython failed')
        except OSError:
            r = subprocess.call((([sys.executable, '-c', 'import sys; from Cython.Compiler.Main import setuptools_main as main; sys.exit(main())'] + flags) + ['-o', tofile, fromfile]))
            if (r != 0):
                raise Exception('Cython failed')
    except OSError:
        raise OSError('Cython needs to be installed')
