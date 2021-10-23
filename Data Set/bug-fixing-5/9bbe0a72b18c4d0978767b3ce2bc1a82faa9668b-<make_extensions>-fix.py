def make_extensions(options, compiler, use_cython):
    'Produce a list of Extension instances which passed to cythonize().'
    no_cuda = options['no_cuda']
    settings = build.get_compiler_setting()
    include_dirs = settings['include_dirs']
    settings['include_dirs'] = [x for x in include_dirs if path.exists(x)]
    settings['library_dirs'] = [x for x in settings['library_dirs'] if path.exists(x)]
    if (sys.platform != 'win32'):
        settings['runtime_library_dirs'] = settings['library_dirs']
    if (sys.platform == 'darwin'):
        args = settings.setdefault('extra_link_args', [])
        args.append(('-Wl,' + ','.join((('-rpath,' + p) for p in settings['library_dirs']))))
        args.append('-mmacosx-version-min=10.5')
    settings['define_macros'].append(('_GLIBCXX_USE_CXX11_ABI', '0'))
    if options['linetrace']:
        settings['define_macros'].append(('CYTHON_TRACE', '1'))
        settings['define_macros'].append(('CYTHON_TRACE_NOGIL', '1'))
    if no_cuda:
        settings['define_macros'].append(('CUPY_NO_CUDA', '1'))
    ret = []
    ext = ('.pyx' if use_cython else '.cpp')
    for module in MODULES:
        print('Include directories:', settings['include_dirs'])
        print('Library directories:', settings['library_dirs'])
        if (not no_cuda):
            if (not check_library(compiler, includes=module['include'], include_dirs=settings['include_dirs'])):
                utils.print_warning(('Include files not found: %s' % module['include']), ('Skip installing %s support' % module['name']), 'Check your CFLAGS environment variable')
                continue
            if (not check_library(compiler, libraries=module['libraries'], library_dirs=settings['library_dirs'])):
                utils.print_warning(('Cannot link libraries: %s' % module['libraries']), ('Skip installing %s support' % module['name']), 'Check your LDFLAGS environment variable')
                continue
            if (('check_method' in module) and (not module['check_method'](compiler, settings))):
                continue
        s = settings.copy()
        if (not no_cuda):
            s['libraries'] = module['libraries']
        if (module['name'] == 'cusolver'):
            args = s.setdefault('extra_link_args', [])
            if ((compiler.compiler_type == 'unix') and (sys.platform != 'darwin')):
                args.append('-fopenmp')
            elif (compiler.compiler_type == 'msvc'):
                args.append('/openmp')
        ret.extend([setuptools.Extension(f, [(path.join(*f.split('.')) + ext)], **s) for f in module['file']])
    return ret