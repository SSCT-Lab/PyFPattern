def maybe_cythonize(extensions, *args, **kwargs):
    '\n    Render tempita templates before calling cythonize. This is skipped for\n\n    * clean\n    * sdist\n    '
    if (('clean' in sys.argv) or ('sdist' in sys.argv)):
        return extensions
    elif (not cython):
        raise RuntimeError('Cannot cythonize without Cython installed.')
    numpy_incl = pkg_resources.resource_filename('numpy', 'core/include')
    for ext in extensions:
        if (hasattr(ext, 'include_dirs') and (numpy_incl not in ext.include_dirs)):
            ext.include_dirs.append(numpy_incl)
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', type=int)
    parser.add_argument('--parallel', type=int)
    (parsed, _) = parser.parse_known_args()
    nthreads = 0
    if parsed.parallel:
        nthreads = parsed.parallel
    elif parsed.j:
        nthreads = parsed.j
    if (is_platform_windows() and (nthreads > 0)):
        print('Parallel build for cythonize ignored on Windows')
        nthreads = 0
    kwargs['nthreads'] = nthreads
    build_ext.render_templates(_pxifiles)
    return cythonize(extensions, *args, **kwargs)