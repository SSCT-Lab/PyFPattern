

def cython(pyx_files, working_path=''):
    'Use Cython to convert the given files to C.\n\n    Parameters\n    ----------\n    pyx_files : list of str\n        The input .pyx files.\n\n    '
    if ((len(sys.argv) >= 2) and (sys.argv[1] == 'clean')):
        return
    try:
        from Cython import __version__
        if (LooseVersion(__version__) < '0.23'):
            raise ImportError
        from Cython.Build import cythonize
    except ImportError:
        c_files = [f.replace('.pyx.in', '.c').replace('.pyx', '.c') for f in pyx_files]
        for cfile in [os.path.join(working_path, f) for f in c_files]:
            if (not os.path.isfile(cfile)):
                raise RuntimeError('Cython >= 0.23 is required to build scikit-image from git checkout')
        print(('Cython >= 0.23 not found; falling back to pre-built %s' % ' '.join(c_files)))
    else:
        for pyxfile in [os.path.join(working_path, f) for f in pyx_files]:
            if (not _changed(pyxfile)):
                continue
            if pyxfile.endswith('.pyx.in'):
                process_tempita_pyx(pyxfile)
                pyxfile = pyxfile.replace('.pyx.in', '.pyx')
            cythonize(pyxfile)
