@utils.memoize
def _ldflags(ldflags_str, libs, flags, libs_dir, include_dir):
    'Extract list of compilation flags from a string.\n\n    Depending on the options, different type of flags will be kept.\n\n    Parameters\n    ----------\n    ldflags_str : string\n        The string to process. Typically, this will be the content of\n        `theano.config.blas.ldflags`.\n    libs : bool\n        Extract flags starting with "-l".\n    flags: bool\n        Extract all the other flags.\n    libs_dir: bool\n        Extract flags starting with "-L".\n    include_dir: bool\n        Extract flags starting with "-I".\n\n    Returns\n    -------\n    list of strings\n        Extracted flags.\n\n    '
    rval = []
    if libs_dir:
        found_dyn = False
        dirs = [x[2:] for x in ldflags_str.split() if x.startswith('-L')]
        l = _ldflags(ldflags_str=ldflags_str, libs=True, flags=False, libs_dir=False, include_dir=False)
        for d in dirs:
            for f in os.listdir(d.strip('"')):
                if (f.endswith('.so') or f.endswith('.dylib') or f.endswith('.dll')):
                    if any([(f.find(ll) >= 0) for ll in l]):
                        found_dyn = True
        if ((not found_dyn) and dirs):
            _logger.warning('We did not found a dynamic library into the library_dir of the library we use for blas. If you use ATLAS, make sure to compile it with dynamics library.')
    for t in ldflags_str.split():
        if ((t.startswith("'") and t.endswith("'")) or (t.startswith('"') and t.endswith('"'))):
            t = t[1:(- 1)]
        try:
            (t0, t1, t2) = t[0:3]
            assert (t0 == '-')
        except Exception:
            raise ValueError(('invalid token "%s" in ldflags_str: "%s"' % (t, ldflags_str)))
        if (libs_dir and (t1 == 'L')):
            rval.append(t[2:])
        elif (include_dir and (t1 == 'I')):
            raise ValueError('Include dirs are not used for blas. We disable this as this can hide other headers and this is not wanted.', t)
            rval.append(t[2:])
        elif (libs and (t1 == 'l')):
            rval.append(t[2:])
        elif (flags and (t1 not in ['L', 'I', 'l'])):
            rval.append(t)
        elif (flags and (t1 == 'L')):
            rval.append(('-Wl,-rpath,' + t[2:]))
    return rval