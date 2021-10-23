

@staticmethod
def compile_str(module_name, src_code, location=None, include_dirs=[], lib_dirs=[], libs=[], preargs=[], rpaths=rpath_defaults, py_module=True, hide_symbols=True):
    '\n\n        Parameters\n        ----------\n        module_name: str\n             This has been embedded in the src_code.\n        src_code\n            A complete c or c++ source listing for the module.\n        location\n            A pre-existing filesystem directory where the\n            cpp file and .so will be written.\n        include_dirs\n            A list of include directory names (each gets prefixed with -I).\n        lib_dirs\n            A list of library search path directory names (each gets\n            prefixed with -L).\n        libs\n            A list of libraries to link with (each gets prefixed with -l).\n        preargs\n            A list of extra compiler arguments.\n        rpaths\n            List of rpaths to use with Xlinker. Defaults to `rpath_defaults`.\n        py_module\n            If False, compile to a shared library, but\n            do not import as a Python module.\n        hide_symbols\n            If True (the default), hide all symbols from the library symbol\n            table unless explicitely exported.\n\n        Returns\n        -------\n        module\n            Dynamically-imported python module of the compiled code.\n            (unless py_module is False, in that case returns None.)\n\n        Notes\n        -----\n        On Windows 7 with nvcc 3.1 we need to compile in the real directory\n        Otherwise nvcc never finish.\n\n        '
    include_dirs = [d for d in include_dirs if d]
    lib_dirs = [d for d in lib_dirs if d]
    rpaths = list(rpaths)
    if (sys.platform == 'win32'):
        for a in ['-Wno-write-strings', '-Wno-unused-label', '-Wno-unused-variable', '-fno-math-errno']:
            if (a in preargs):
                preargs.remove(a)
    if (preargs is None):
        preargs = []
    else:
        preargs = list(preargs)
    if (sys.platform != 'win32'):
        preargs.append('-fPIC')
    if config.cmodule.remove_gxx_opt:
        preargs = [p for p in preargs if (not p.startswith('-O'))]
    cuda_root = config.cuda.root
    include_dirs = (include_dirs + std_include_dirs())
    if (os.path.abspath(os.path.split(__file__)[0]) not in include_dirs):
        include_dirs.append(os.path.abspath(os.path.split(__file__)[0]))
    libs = (libs + std_libs())
    if ('cudart' not in libs):
        libs.append('cudart')
    lib_dirs = (lib_dirs + std_lib_dirs())
    if (sys.platform != 'darwin'):
        lib_dirs = [ld for ld in lib_dirs if (not ((ld == os.path.join(cuda_root, 'lib')) or (ld == os.path.join(cuda_root, 'lib64'))))]
    if (sys.platform != 'darwin'):
        python_lib = distutils.sysconfig.get_python_lib(plat_specific=1, standard_lib=1)
        python_lib = os.path.dirname(python_lib)
        if (python_lib not in lib_dirs):
            lib_dirs.append(python_lib)
    cppfilename = os.path.join(location, 'mod.cu')
    with open(cppfilename, 'w') as cppfile:
        _logger.debug('Writing module C++ code to %s', cppfilename)
        cppfile.write(src_code)
    lib_filename = os.path.join(location, ('%s.%s' % (module_name, get_lib_extension())))
    _logger.debug('Generating shared lib %s', lib_filename)
    preargs1 = []
    preargs2 = []
    for pa in preargs:
        if pa.startswith('-Wl,'):
            if ((sys.platform != 'win32') or (not pa.startswith('-Wl,-rpath'))):
                preargs1.append('-Xlinker')
                preargs1.append(pa[4:])
            continue
        for pattern in ['-O', '-arch=', '-ccbin=', '-G', '-g', '-I', '-L', '--fmad', '--ftz', '--maxrregcount', '--prec-div', '--prec-sqrt', '--use_fast_math', '-fmad', '-ftz', '-maxrregcount', '-prec-div', '-prec-sqrt', '-use_fast_math', '--use-local-env', '--cl-version=']:
            if pa.startswith(pattern):
                preargs1.append(pa)
                break
        else:
            preargs2.append(pa)
    cmd = ([nvcc_path, '-shared'] + preargs1)
    if config.nvcc.compiler_bindir:
        cmd.extend(['--compiler-bindir', config.nvcc.compiler_bindir])
    if (sys.platform == 'win32'):
        preargs2.extend(['/Zi', '/MD'])
        cmd.extend(['-Xlinker', '/DEBUG'])
        cmd.extend(['-D HAVE_ROUND'])
    elif hide_symbols:
        preargs2.append('-fvisibility=hidden')
    if (local_bitwidth() == 64):
        cmd.append('-m64')
    else:
        cmd.append('-m32')
    if (len(preargs2) > 0):
        cmd.extend(['-Xcompiler', ','.join(preargs2)])
    if ((not type(config.cuda).root.is_default) and os.path.exists(os.path.join(config.cuda.root, 'lib'))):
        rpaths.append(os.path.join(config.cuda.root, 'lib'))
        if (sys.platform != 'darwin'):
            rpaths.append(os.path.join(config.cuda.root, 'lib64'))
    if (sys.platform != 'win32'):
        for rpath in rpaths:
            cmd.extend(['-Xlinker', ','.join(['-rpath', rpath])])
    cmd.extend((('-I%s' % idir) for idir in include_dirs))
    cmd.extend(['-o', lib_filename])
    cmd.append(os.path.split(cppfilename)[(- 1)])
    cmd.extend([('-L%s' % ldir) for ldir in lib_dirs])
    cmd.extend([('-l%s' % l) for l in libs])
    if (sys.platform == 'darwin'):
        cmd.extend(['-Xcompiler', '-undefined,dynamic_lookup'])
    done = False
    while (not done):
        try:
            indexof = cmd.index('-u')
            cmd.pop(indexof)
            cmd.pop(indexof)
        except ValueError:
            done = True
    if ((sys.platform == 'darwin') and (nvcc_version >= '4.1')):
        cmd.extend(['-Xlinker', '-pie'])
    _logger.debug('Running cmd %s', ' '.join(cmd))
    orig_dir = os.getcwd()
    try:
        os.chdir(location)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (nvcc_stdout_raw, nvcc_stderr_raw) = p.communicate()[:2]
        console_encoding = getpreferredencoding()
        nvcc_stdout = decode_with(nvcc_stdout_raw, console_encoding)
        nvcc_stderr = decode_with(nvcc_stderr_raw, console_encoding)
    finally:
        os.chdir(orig_dir)
    for eline in nvcc_stderr.split('\n'):
        if (not eline):
            continue
        if ('skipping incompatible' in eline):
            continue
        if ('declared but never referenced' in eline):
            continue
        if ('statement is unreachable' in eline):
            continue
        _logger.info('NVCC: %s', eline)
    if p.returncode:
        for (i, l) in enumerate(src_code.split('\n')):
            print((i + 1), l, file=sys.stderr)
        print('===============================', file=sys.stderr)
        for l in nvcc_stderr.split('\n'):
            if (not l):
                continue
            try:
                if l[l.index(':'):].startswith(': warning: variable'):
                    continue
                if l[l.index(':'):].startswith(': warning: label'):
                    continue
            except Exception:
                pass
            print(l, file=sys.stderr)
        print(nvcc_stdout)
        print(cmd)
        raise Exception('nvcc return status', p.returncode, 'for cmd', ' '.join(cmd))
    elif (config.cmodule.compilation_warning and nvcc_stdout):
        print(nvcc_stdout)
    if ((sys.platform != 'win32') and nvcc_stdout):
        print('DEBUG: nvcc STDOUT', nvcc_stdout, file=sys.stderr)
    if py_module:
        open(os.path.join(location, '__init__.py'), 'w').close()
        return dlimport(lib_filename)
