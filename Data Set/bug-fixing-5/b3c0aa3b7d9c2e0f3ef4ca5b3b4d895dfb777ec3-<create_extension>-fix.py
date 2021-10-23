def create_extension(name, headers, sources, verbose=True, with_cuda=False, package=False, relative_to='.', **kwargs):
    "Creates and configures a cffi.FFI object, that builds PyTorch extension.\n\n    Arguments:\n        name (str): package name. Can be a nested module e.g. ``.ext.my_lib``.\n        headers (str or List[str]): list of headers, that contain only exported\n            functions\n        sources (List[str]): list of sources to compile.\n        verbose (bool, optional): if set to ``False``, no output will be printed\n            (default: True).\n        with_cuda (bool, optional): set to ``True`` to compile with CUDA headers\n            (default: False)\n        package (bool, optional): set to ``True`` to build in package mode (for modules\n            meant to be installed as pip packages) (default: False).\n        relative_to (str, optional): path of the build file. Required when\n            ``package is True``. It's best to use ``__file__`` for this argument.\n        kwargs: additional arguments that are passed to ffi to declare the\n            extension. See `Extension API reference`_ for details.\n\n    .. _`Extension API reference`: https://docs.python.org/3/distutils/apiref.html#distutils.core.Extension\n    "
    base_path = os.path.abspath(os.path.dirname(relative_to))
    (name_suffix, target_dir) = _create_module_dir(base_path, name)
    if (not package):
        cffi_wrapper_name = ('_' + name_suffix)
    else:
        cffi_wrapper_name = (name.rpartition('.')[0] + '.{0}._{0}'.format(name_suffix))
    (wrapper_source, include_dirs) = _setup_wrapper(with_cuda)
    include_dirs.extend(kwargs.pop('include_dirs', []))
    if isinstance(headers, str):
        headers = [headers]
    all_headers_source = ''
    for header in headers:
        with open(os.path.join(base_path, header), 'r') as f:
            all_headers_source += (f.read() + '\n\n')
    ffi = cffi.FFI()
    sources = [os.path.join(base_path, src) for src in sources]
    ffi.set_source(cffi_wrapper_name, (wrapper_source + all_headers_source), sources=sources, include_dirs=include_dirs, **kwargs)
    ffi.cdef((_typedefs + all_headers_source))
    _make_python_wrapper(name_suffix, ('_' + name_suffix), target_dir)

    def build():
        _build_extension(ffi, cffi_wrapper_name, target_dir, verbose)
    ffi.build = build
    return ffi