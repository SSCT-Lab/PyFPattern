

def build_project(args):
    '\n    Build a dev version of the project.\n\n    Returns\n    -------\n    site_dir\n        site-packages directory where it was installed\n\n    '
    import distutils.sysconfig
    root_ok = [os.path.exists(os.path.join(ROOT_DIR, fn)) for fn in PROJECT_ROOT_FILES]
    if (not all(root_ok)):
        print('To build the project, run runtests.py in git checkout or unpacked source')
        sys.exit(1)
    dst_dir = os.path.join(ROOT_DIR, 'build', 'testenv')
    env = dict(os.environ)
    cmd = [sys.executable, 'setup.py']
    env['PATH'] = os.pathsep.join((EXTRA_PATH + env.get('PATH', '').split(os.pathsep)))
    cvars = distutils.sysconfig.get_config_vars()
    if ('gcc' in cvars.get('CC', '')):
        if ((sys.platform != 'darwin') or ('gnu-gcc' in cvars.get('CC', ''))):
            warnings_as_errors = ' '.join(['-Werror=declaration-after-statement', '-Werror=vla', '-Werror=nonnull', '-Werror=pointer-arith', '-Wlogical-op', '-Werror=unused-function'])
            env['CFLAGS'] = ((warnings_as_errors + ' ') + env.get('CFLAGS', ''))
    if (args.debug or args.gcov):
        env['OPT'] = '-O0 -ggdb'
        env['FOPT'] = '-O0 -ggdb'
        if args.gcov:
            env['OPT'] = '-O0 -ggdb'
            env['FOPT'] = '-O0 -ggdb'
            env['CC'] = (cvars['CC'] + ' --coverage')
            env['CXX'] = (cvars['CXX'] + ' --coverage')
            env['F77'] = 'gfortran --coverage '
            env['F90'] = 'gfortran --coverage '
            env['LDSHARED'] = (cvars['LDSHARED'] + ' --coverage')
            env['LDFLAGS'] = (' '.join(cvars['LDSHARED'].split()[1:]) + ' --coverage')
    cmd += ['build']
    if (args.parallel > 1):
        cmd += ['-j', str(args.parallel)]
    cmd += ['install', ('--prefix=' + dst_dir), '--single-version-externally-managed', (('--record=' + dst_dir) + 'tmp_install_log.txt')]
    from distutils.sysconfig import get_python_lib
    site_dir = get_python_lib(prefix=dst_dir, plat_specific=True)
    site_dir_noarch = get_python_lib(prefix=dst_dir, plat_specific=False)
    if (not os.path.exists(site_dir)):
        os.makedirs(site_dir)
    if (not os.path.exists(site_dir_noarch)):
        os.makedirs(site_dir_noarch)
    env['PYTHONPATH'] = ((site_dir + ':') + site_dir_noarch)
    log_filename = os.path.join(ROOT_DIR, 'build.log')
    if args.show_build_log:
        ret = subprocess.call(cmd, env=env, cwd=ROOT_DIR)
    else:
        log_filename = os.path.join(ROOT_DIR, 'build.log')
        print('Building, see build.log...')
        with open(log_filename, 'w') as log:
            p = subprocess.Popen(cmd, env=env, stdout=log, stderr=log, cwd=ROOT_DIR)
        try:
            last_blip = time.time()
            last_log_size = os.stat(log_filename).st_size
            while (p.poll() is None):
                time.sleep(0.5)
                if ((time.time() - last_blip) > 60):
                    log_size = os.stat(log_filename).st_size
                    if (log_size > last_log_size):
                        print('    ... build in progress')
                        last_blip = time.time()
                        last_log_size = log_size
            ret = p.wait()
        except:
            p.kill()
            p.wait()
            raise
    if (ret == 0):
        print('Build OK')
    else:
        if (not args.show_build_log):
            with open(log_filename, 'r') as f:
                print(f.read())
            print('Build failed!')
        sys.exit(1)
    return (site_dir, site_dir_noarch)
