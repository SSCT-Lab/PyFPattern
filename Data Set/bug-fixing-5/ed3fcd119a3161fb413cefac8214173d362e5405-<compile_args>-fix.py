@staticmethod
def compile_args(march_flags=True):
    cxxflags = [flag for flag in config.gcc.cxxflags.split(' ') if flag]
    detect_march = ((GCC_compiler.march_flags is None) and march_flags)
    if detect_march:
        for f in cxxflags:
            if (f.startswith('--march=') or f.startswith('-march=')):
                _logger.warn("WARNING: your Theano flags `gcc.cxxflags` specify an `-march=X` flags.\n         It is better to let Theano/g++ find it automatically, but we don't do it now")
                detect_march = False
                GCC_compiler.march_flags = []
                break
    if (('g++' not in theano.config.cxx) and ('clang++' not in theano.config.cxx) and ('clang-omp++' not in theano.config.cxx) and ('icpc' not in theano.config.cxx)):
        _logger.warn('OPTIMIZATION WARNING: your Theano flag `cxx` seems not to be the g++ compiler. So we disable the compiler optimization specific to g++ that tell to compile for a specific CPU. At worst, this could cause slow down.\n         You can add those parameters to the compiler yourself via the Theano flag `gcc.cxxflags`.')
        detect_march = False
    if detect_march:
        GCC_compiler.march_flags = []

        def get_lines(cmd, parse=True):
            p = subprocess_Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
            (stdout, stderr) = p.communicate(input=b(''))
            if (p.returncode != 0):
                return None
            lines = BytesIO((stdout + stderr)).readlines()
            lines = decode_iter(lines)
            if parse:
                selected_lines = []
                for line in lines:
                    if (('COLLECT_GCC_OPTIONS=' in line) or ('CFLAGS=' in line) or ('CXXFLAGS=' in line) or ('-march=native' in line)):
                        continue
                    for reg in ['-march=', '-mtune=', '-target-cpu', '-mabi=']:
                        if (reg in line):
                            selected_lines.append(line.strip())
                lines = list(set(selected_lines))
            return lines
        native_lines = get_lines(('%s -march=native -E -v -' % theano.config.cxx))
        if (native_lines is None):
            _logger.info("Call to 'g++ -march=native' failed,not setting -march flag")
            detect_march = False
        else:
            _logger.info('g++ -march=native selected lines: %s', native_lines)
    if detect_march:
        if (len(native_lines) != 1):
            if (len(native_lines) == 0):
                reported_lines = get_lines(('%s -march=native -E -v -' % theano.config.cxx), parse=False)
            else:
                reported_lines = native_lines
            _logger.warn("OPTIMIZATION WARNING: Theano was not able to find the g++ parameters that tune the compilation to your  specific CPU. This can slow down the execution of Theano functions. Please submit the following lines to Theano's mailing list so that we can fix this problem:\n %s", reported_lines)
        else:
            default_lines = get_lines(('%s -E -v -' % theano.config.cxx))
            _logger.info('g++ default lines: %s', default_lines)
            if (len(default_lines) < 1):
                _logger.warn("OPTIMIZATION WARNING: Theano was not able to find the default g++ parameters. This is needed to tune the compilation to your specific CPU. This can slow down the execution of Theano functions. Please submit the following lines to Theano's mailing list so that we can fix this problem:\n %s", get_lines(('%s -E -v -' % theano.config.cxx), parse=False))
            else:

                def join_options(init_part):
                    new_part = []
                    for i in range(len(init_part)):
                        p = init_part[i]
                        if p.startswith('-'):
                            p_list = [p]
                            while (((i + 1) < len(init_part)) and (not init_part[(i + 1)].startswith('-'))):
                                p_list.append(init_part[(i + 1)])
                                i += 1
                            new_part.append(' '.join(p_list))
                        elif (i == 0):
                            new_part.append(p)
                    return new_part
                part = join_options(native_lines[0].split())
                for line in default_lines:
                    if line.startswith(part[0]):
                        part2 = [p for p in join_options(line.split()) if (('march' not in p) and ('mtune' not in p) and ('target-cpu' not in p))]
                        if (sys.platform == 'darwin'):
                            new_flags = [p for p in part if ('target-cpu' in p)]
                        else:
                            new_flags = [p for p in part if (p not in part2)]
                        for (i, p) in enumerate(new_flags):
                            if ('target-cpu' in p):
                                opt = p.split()
                                if (len(opt) == 2):
                                    (opt_name, opt_val) = opt
                                    new_flags[i] = ('-march=%s' % opt_val)
                        for (i, p) in enumerate(new_flags):
                            if ('march' not in p):
                                continue
                            opt = p.split('=')
                            if (len(opt) != 2):
                                continue
                            opt_val = opt[1]
                            if (not opt_val.endswith('-avx')):
                                continue
                            version = gcc_version_str.split('.')
                            if (len(version) != 3):
                                continue
                            (mj, mn, patch) = [int(vp) for vp in version]
                            if ((((mj, mn) == (4, 6)) and (patch < 4)) or (((mj, mn) == (4, 7)) and (patch <= 3)) or (((mj, mn) == (4, 8)) and (patch < 1))):
                                new_flags[i] = p.rstrip('-avx')
                        split_flags = []
                        for p in new_flags:
                            split_flags.extend(p.split())
                        GCC_compiler.march_flags = split_flags
                        break
                _logger.info('g++ -march=native equivalent flags: %s', GCC_compiler.march_flags)
        (default_compilation_result, default_execution_result) = try_march_flag(GCC_compiler.march_flags)
        if ((not default_compilation_result) or (not default_execution_result)):
            march_success = False
            march_ind = None
            mtune_ind = None
            default_detected_flag = []
            march_flags_to_try = ['corei7-avx', 'corei7', 'core2']
            for m_ in xrange(len(GCC_compiler.march_flags)):
                march_flag = GCC_compiler.march_flags[m_]
                if ('march' in march_flag):
                    march_ind = m_
                    default_detected_flag = [march_flag]
                elif ('mtune' in march_flag):
                    mtune_ind = m_
            for march_flag in march_flags_to_try:
                if (march_ind is not None):
                    GCC_compiler.march_flags[march_ind] = ('-march=' + march_flag)
                if (mtune_ind is not None):
                    GCC_compiler.march_flags[mtune_ind] = ('-mtune=' + march_flag)
                (compilation_result, execution_result) = try_march_flag(GCC_compiler.march_flags)
                if (compilation_result and execution_result):
                    march_success = True
                    break
            if (not march_success):
                march_flags_to_try = (default_detected_flag + march_flags_to_try)
                for march_flag in march_flags_to_try:
                    (compilation_result, execution_result) = try_march_flag([('-march=' + march_flag)])
                    if (compilation_result and execution_result):
                        march_success = True
                        GCC_compiler.march_flags = [('-march=' + march_flag)]
                        break
            if (not march_success):
                GCC_compiler.march_flags = []
    if (march_flags and GCC_compiler.march_flags):
        cxxflags.extend(GCC_compiler.march_flags)
    cxxflags.append('-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION')
    numpy_ver = [int(n) for n in numpy.__version__.split('.')[:2]]
    if bool((numpy_ver < [1, 7])):
        cxxflags.append('-DNPY_ARRAY_ENSUREARRAY=NPY_ENSUREARRAY')
        cxxflags.append('-DNPY_ARRAY_ENSURECOPY=NPY_ENSURECOPY')
        cxxflags.append('-DNPY_ARRAY_ALIGNED=NPY_ALIGNED')
        cxxflags.append('-DNPY_ARRAY_WRITEABLE=NPY_WRITEABLE')
        cxxflags.append('-DNPY_ARRAY_UPDATE_ALL=NPY_UPDATE_ALL')
        cxxflags.append('-DNPY_ARRAY_C_CONTIGUOUS=NPY_C_CONTIGUOUS')
        cxxflags.append('-DNPY_ARRAY_F_CONTIGUOUS=NPY_F_CONTIGUOUS')
    if ((not any([('arm' in flag) for flag in cxxflags])) and (not any(((arch in platform.machine()) for arch in ['arm', 'aarch'])))):
        n_bits = local_bitwidth()
        cxxflags.append(('-m%d' % n_bits))
        _logger.debug('Compiling for %s bit architecture', n_bits)
    if (sys.platform != 'win32'):
        cxxflags.append('-fPIC')
    if ((sys.platform == 'win32') and (local_bitwidth() == 64)):
        cxxflags.append('-DMS_WIN64')
    if (sys.platform == 'darwin'):
        cxxflags.extend(['-undefined', 'dynamic_lookup'])
    return cxxflags