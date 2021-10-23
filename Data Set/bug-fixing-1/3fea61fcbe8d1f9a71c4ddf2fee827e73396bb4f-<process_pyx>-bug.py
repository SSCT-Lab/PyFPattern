

def process_pyx(fromfile, tofile):
    flags = ['-3', '--fast-fail']
    if tofile.endswith('.cxx'):
        flags.append('--cplus')
    try:
        from Cython.Compiler.Version import version as cython_version
    except ImportError:
        try:
            subprocess.check_call(((['cython'] + flags) + ['-o', tofile, fromfile]))
        except OSError:
            raise OSError('Cython needs to be installed')
    else:
        from distutils.version import LooseVersion
        required_version = LooseVersion('0.29.13')
        if (LooseVersion(cython_version) < required_version):
            raise RuntimeError('Building {} requires Cython >= {}'.format(VENDOR, required_version))
        subprocess.check_call((([sys.executable, '-m', 'cython'] + flags) + ['-o', tofile, fromfile]))
