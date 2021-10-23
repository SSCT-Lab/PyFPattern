def get_cxx_std_flag(compiler):
    'Detects compiler flag for c++14, c++11 or None if not detected'
    gnu_flags = ['--std=c++14', '--std=c++11']
    flags_by_cc = {
        'msvc': ['/std:c++14', None],
        'intelw': ['/Qstd=c++14', '/Qstd=c++11'],
    }
    flags = flags_by_cc.get(compiler.compiler_type, gnu_flags)
    for flag in flags:
        if (flag is None):
            return None
        if has_flag(compiler, flag):
            return flag
    from numpy.distutils import log
    log.warn('Could not detect c++ standard flag')
    return None