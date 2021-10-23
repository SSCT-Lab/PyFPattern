def main(argv):
    parser = ArgumentParser(usage=__doc__.lstrip())
    parser.add_argument('--verbose', '-v', action='count', default=1, help='more verbosity')
    parser.add_argument('--no-build', '-n', action='store_true', default=False, help='do not build the project (use system installed version)')
    parser.add_argument('--build-only', '-b', action='store_true', default=False, help='just build, do not run any tests')
    parser.add_argument('--doctests', action='store_true', default=False, help='Run doctests in module')
    parser.add_argument('--refguide-check', action='store_true', default=False, help='Run refguide check (do not run regular tests.)')
    parser.add_argument('--coverage', action='store_true', default=False, help='report coverage of project code. HTML output goes under build/coverage')
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
    parser.add_argument('--parallel', '-j', type=int, default=1, help='Number of parallel jobs during build (requires NumPy 1.10 or greater).')
    parser.add_argument('--show-build-log', action='store_true', help='Show build output rather than using a log file')
    parser.add_argument('--bench', action='store_true', help='Run benchmark suite instead of test suite')
    parser.add_argument('--bench-compare', action='append', metavar='BEFORE', help='Compare benchmark results of current HEAD to BEFORE. Use an additional --bench-compare=COMMIT to override HEAD with COMMIT. Note that you need to commit your changes first!')
    parser.add_argument('args', metavar='ARGS', default=[], nargs=REMAINDER, help='Arguments to pass to Nose, Python or shell')
    args = parser.parse_args(argv)
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
        site_dir = build_project(args)
        sys.path.insert(0, site_dir)
        os.environ['PYTHONPATH'] = site_dir
    extra_argv = args.args[:]
    if (extra_argv and (extra_argv[0] == '--')):
        extra_argv = extra_argv[1:]
    if args.python:
        if extra_argv:
            sys.argv = extra_argv
            with open(extra_argv[0], 'r') as f:
                script = f.read()
            sys.modules['__main__'] = new_module('__main__')
            ns = dict(__name__='__main__', __file__=extra_argv[0])
            exec_(script, ns)
            sys.exit(0)
        else:
            import code
            code.interact()
            sys.exit(0)
    if args.ipython:
        import IPython
        IPython.embed(user_ns={
            
        })
        sys.exit(0)
    if args.shell:
        shell = os.environ.get('SHELL', 'sh')
        print('Spawning a Unix shell...')
        os.execv(shell, ([shell] + extra_argv))
        sys.exit(1)
    if args.coverage:
        dst_dir = os.path.join(ROOT_DIR, 'build', 'coverage')
        fn = os.path.join(dst_dir, 'coverage_html.js')
        if (os.path.isdir(dst_dir) and os.path.isfile(fn)):
            shutil.rmtree(dst_dir)
        extra_argv += [('--cov-report=html:' + dst_dir)]
    if args.refguide_check:
        cmd = [os.path.join(ROOT_DIR, 'tools', 'refguide_check.py'), '--doctests']
        if args.submodule:
            cmd += [args.submodule]
        os.execv(sys.executable, ([sys.executable] + cmd))
        sys.exit(0)
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
            cmd = ([os.path.join(ROOT_DIR, 'benchmarks', 'run.py'), 'run', '-n', '-e', '--python=same'] + bench_args)
            os.execv(sys.executable, ([sys.executable] + cmd))
            sys.exit(1)
        else:
            if (len(args.bench_compare) == 1):
                commit_a = args.bench_compare[0]
                commit_b = 'HEAD'
            elif (len(args.bench_compare) == 2):
                (commit_a, commit_b) = args.bench_compare
            else:
                p.error('Too many commits to compare benchmarks for')
            if (commit_b == 'HEAD'):
                r1 = subprocess.call(['git', 'diff-index', '--quiet', '--cached', 'HEAD'])
                r2 = subprocess.call(['git', 'diff-files', '--quiet'])
                if ((r1 != 0) or (r2 != 0)):
                    print(('*' * 80))
                    print('WARNING: you have uncommitted changes --- these will NOT be benchmarked!')
                    print(('*' * 80))
            p = subprocess.Popen(['git', 'rev-parse', commit_b], stdout=subprocess.PIPE)
            (out, err) = p.communicate()
            commit_b = out.strip()
            p = subprocess.Popen(['git', 'rev-parse', commit_a], stdout=subprocess.PIPE)
            (out, err) = p.communicate()
            commit_a = out.strip()
            cmd = ([os.path.join(ROOT_DIR, 'benchmarks', 'run.py'), 'continuous', '-e', '-f', '1.05', commit_a, commit_b] + bench_args)
            os.execv(sys.executable, ([sys.executable] + cmd))
            sys.exit(1)
    if args.build_only:
        sys.exit(0)
    else:
        __import__(PROJECT_MODULE)
        test = sys.modules[PROJECT_MODULE].test
    if args.submodule:
        tests = [((PROJECT_MODULE + '.') + args.submodule)]
    elif args.tests:
        tests = args.tests
    else:
        tests = None
    if (not args.no_build):
        test_dir = site_dir
    else:
        test_dir = os.path.join(ROOT_DIR, 'build', 'test')
        if (not os.path.isdir(test_dir)):
            os.makedirs(test_dir)
    shutil.copyfile(os.path.join(ROOT_DIR, '.coveragerc'), os.path.join(test_dir, '.coveragerc'))
    cwd = os.getcwd()
    try:
        os.chdir(test_dir)
        result = test(args.mode, verbose=args.verbose, extra_argv=extra_argv, doctests=args.doctests, coverage=args.coverage, tests=tests, parallel=args.parallel)
    finally:
        os.chdir(cwd)
    if isinstance(result, bool):
        sys.exit((0 if result else 1))
    elif result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)