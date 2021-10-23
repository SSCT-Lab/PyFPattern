

def main(argv):
    parser = ArgumentParser(usage=__doc__.lstrip())
    parser.add_argument('--verbose', '-v', action='count', default=1, help='more verbosity')
    parser.add_argument('--no-build', '-n', action='store_true', default=False, help='do not build the project (use system installed version)')
    parser.add_argument('--build-only', '-b', action='store_true', default=False, help='just build, do not run any tests')
    parser.add_argument('--doctests', action='store_true', default=False, help='Run doctests in module')
    parser.add_argument('--coverage', action='store_true', default=False, help='report coverage of project code. HTML output goes under build/coverage')
    parser.add_argument('--timer', action='store', default=0, type=int, help='Time N slowest test')
    parser.add_argument('--gcov', action='store_true', default=False, help='enable C code coverage via gcov (requires GCC). gcov output goes to build/**/*.gc*')
    parser.add_argument('--lcov-html', action='store_true', default=False, help='produce HTML for C code coverage information from a previous run with --gcov. HTML output goes to build/lcov/')
    parser.add_argument('--mode', '-m', default='fast', help="'fast', 'full', or something that could be passed to nosetests -A [default: fast]")
    parser.add_argument('--submodule', '-s', default=None, help='Submodule whose tests to run (cluster, constants, ...)')
    parser.add_argument('--pythonpath', '-p', default=None, help='Paths to prepend to PYTHONPATH')
    parser.add_argument('--tests', '-t', action='append', help='Specify tests to run')
    parser.add_argument('--python', action='store_true', help='Start a Python shell with PYTHONPATH set')
    parser.add_argument('--ipython', '-i', action='store_true', help='Start IPython shell with PYTHONPATH set')
    parser.add_argument('--shell', action='store_true', help='Start Unix shell with PYTHONPATH set')
    parser.add_argument('--debug', '-g', action='store_true', help='Debug build')
    parser.add_argument('--parallel', '-j', type=int, default=0, help='Number of parallel jobs during build')
    parser.add_argument('--show-build-log', action='store_true', help='Show build output rather than using a log file')
    parser.add_argument('--bench', action='store_true', help='Run benchmark suite instead of test suite')
    parser.add_argument('--bench-compare', action='store', metavar='COMMIT', help='Compare benchmark results to COMMIT. Note that you need to commit your changes first!')
    parser.add_argument('--raise-warnings', default=None, type=str, choices=('develop', 'release'), help="if 'develop', warnings are treated as errors; defaults to 'develop' in development versions.")
    parser.add_argument('args', metavar='ARGS', default=[], nargs=REMAINDER, help='Arguments to pass to Nose, Python or shell')
    args = parser.parse_args(argv)
    if (args.timer == 0):
        timer = False
    elif (args.timer == (- 1)):
        timer = True
    elif (args.timer > 0):
        timer = int(args.timer)
    else:
        raise ValueError('--timer value should be an integer, -1 or >0')
    args.timer = timer
    if args.bench_compare:
        args.bench = True
        args.no_build = True
    if args.lcov_html:
        lcov_generate()
        sys.exit(0)
    if args.pythonpath:
        for p in reversed(args.pythonpath.split(os.pathsep)):
            sys.path.insert(0, p)
    if args.gcov:
        gcov_reset_counters()
    if (args.debug and args.bench):
        print('*** Benchmarks should not be run against debug version; remove -g flag ***')
    if (not args.no_build):
        (site_dir, site_dir_noarch) = build_project(args)
        sys.path.insert(0, site_dir)
        sys.path.insert(0, site_dir_noarch)
        os.environ['PYTHONPATH'] = ((site_dir + os.pathsep) + site_dir_noarch)
    extra_argv = args.args[:]
    if (extra_argv and (extra_argv[0] == '--')):
        extra_argv = extra_argv[1:]
    if args.python:
        print('Enabling display of all warnings')
        import warnings
        import types
        warnings.filterwarnings('always')
        if extra_argv:
            sys.argv = extra_argv
            with open(extra_argv[0], 'r') as f:
                script = f.read()
            sys.modules['__main__'] = types.ModuleType('__main__')
            ns = dict(__name__='__main__', __file__=extra_argv[0])
            exec_(script, ns)
            sys.exit(0)
        else:
            import code
            code.interact()
            sys.exit(0)
    if args.ipython:
        print('Enabling display of all warnings and pre-importing numpy as np')
        import warnings
        warnings.filterwarnings('always')
        import IPython
        import numpy as np
        IPython.embed(user_ns={
            'np': np,
        })
        sys.exit(0)
    if args.shell:
        shell = os.environ.get('SHELL', ('cmd' if (os.name == 'nt') else 'sh'))
        print('Spawning a shell ({})...'.format(shell))
        subprocess.call(([shell] + extra_argv))
        sys.exit(0)
    if args.coverage:
        dst_dir = os.path.join(ROOT_DIR, 'build', 'coverage')
        fn = os.path.join(dst_dir, 'coverage_html.js')
        if (os.path.isdir(dst_dir) and os.path.isfile(fn)):
            shutil.rmtree(dst_dir)
        extra_argv += ['--cover-html', ('--cover-html-dir=' + dst_dir)]
    if args.bench:
        items = extra_argv
        if args.tests:
            items += args.tests
        if args.submodule:
            items += [args.submodule]
        bench_args = []
        for a in items:
            bench_args.extend(['--bench', a])
        if (not args.bench_compare):
            cmd = (['asv', 'run', '-n', '-e', '--python=same'] + bench_args)
            ret = subprocess.call(cmd, cwd=os.path.join(ROOT_DIR, 'benchmarks'))
            sys.exit(ret)
        else:
            commits = [x.strip() for x in args.bench_compare.split(',')]
            if (len(commits) == 1):
                commit_a = commits[0]
                commit_b = 'HEAD'
            elif (len(commits) == 2):
                (commit_a, commit_b) = commits
            else:
                p.error('Too many commits to compare benchmarks for')
            if (commit_b == 'HEAD'):
                r1 = subprocess.call(['git', 'diff-index', '--quiet', '--cached', 'HEAD'])
                r2 = subprocess.call(['git', 'diff-files', '--quiet'])
                if ((r1 != 0) or (r2 != 0)):
                    print(('*' * 80))
                    print('WARNING: you have uncommitted changes --- these will NOT be benchmarked!')
                    print(('*' * 80))
            out = subprocess.check_output(['git', 'rev-parse', commit_b])
            commit_b = out.strip()
            out = subprocess.check_output(['git', 'rev-parse', commit_a])
            commit_a = out.strip()
            cmd = (['asv', 'continuous', '-e', '-f', '1.05', commit_a, commit_b] + bench_args)
            ret = subprocess.call(cmd, cwd=os.path.join(ROOT_DIR, 'benchmarks'))
            sys.exit(ret)
    test_dir = os.path.join(ROOT_DIR, 'build', 'test')
    if args.build_only:
        sys.exit(0)
    elif args.submodule:
        modname = ((PROJECT_MODULE + '.') + args.submodule)
        try:
            __import__(modname)
            test = sys.modules[modname].test
        except (ImportError, KeyError, AttributeError):
            print(('Cannot run tests for %s' % modname))
            sys.exit(2)
    elif args.tests:

        def fix_test_path(x):
            p = x.split(':')
            p[0] = os.path.relpath(os.path.abspath(p[0]), test_dir)
            return ':'.join(p)
        tests = [fix_test_path(x) for x in args.tests]

        def test(*a, **kw):
            extra_argv = kw.pop('extra_argv', ())
            extra_argv = (extra_argv + tests[1:])
            kw['extra_argv'] = extra_argv
            import numpy as np
            from numpy.testing import Tester
            if (kw['raise_warnings'] is None):
                if (hasattr(np, '__version__') and ('.dev0' in np.__version__)):
                    kw['raise_warnings'] = 'develop'
                else:
                    kw['raise_warnings'] = 'release'
            return Tester(tests[0]).test(*a, **kw)
    else:
        __import__(PROJECT_MODULE)
        test = sys.modules[PROJECT_MODULE].test
    try:
        shutil.rmtree(test_dir)
    except OSError:
        pass
    try:
        os.makedirs(test_dir)
    except OSError:
        pass
    cwd = os.getcwd()
    try:
        os.chdir(test_dir)
        result = test(args.mode, verbose=args.verbose, extra_argv=extra_argv, doctests=args.doctests, raise_warnings=args.raise_warnings, coverage=args.coverage, timer=args.timer)
    finally:
        os.chdir(cwd)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
