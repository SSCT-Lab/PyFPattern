def compile_with_cache(source, options=(), arch=None, cache_dir=None):
    global _empty_file_preprocess_cache
    if (cache_dir is None):
        cache_dir = get_cache_dir()
    if (arch is None):
        arch = _get_arch()
    if ('win32' == sys.platform):
        options += ('-Xcompiler', '/wd 4819')
        if (sys.maxsize == 9223372036854775807):
            options += ('-m64',)
        elif (sys.maxsize == 2147483647):
            options += ('-m32',)
    env = (arch, options, _get_nvcc_version())
    if ('#include' in source):
        pp_src = ('%s %s' % (env, preprocess(source, options)))
    else:
        base = _empty_file_preprocess_cache.get(env, None)
        if (base is None):
            base = _empty_file_preprocess_cache[env] = preprocess('', options)
        pp_src = ('%s %s %s' % (env, base, source))
    if isinstance(pp_src, six.text_type):
        pp_src = pp_src.encode('utf-8')
    name = ('%s.cubin' % hashlib.md5(pp_src).hexdigest())
    mod = function.Module()
    if (not os.path.exists(cache_dir)):
        os.makedirs(cache_dir)
    lock_path = os.path.join(cache_dir, 'lock_file.lock')
    path = os.path.join(cache_dir, name)
    with filelock.FileLock(lock_path) as lock:
        if os.path.exists(path):
            with open(path, 'rb') as file:
                cubin = file.read()
            mod.load(cubin)
        else:
            lock.release()
            cubin = nvcc(source, options, arch)
            mod.load(cubin)
            lock.acquire()
            with open(path, 'wb') as cubin_file:
                cubin_file.write(cubin)
    return mod