def test_distributed(python, test_module, test_directory, options):
    mpi_available = (subprocess.call('command -v mpiexec', shell=True) == 0)
    if (options.verbose and (not mpi_available)):
        print_to_stderr('MPI not available -- MPI backend tests will be skipped')
    for (backend, env_vars) in DISTRIBUTED_TESTS_CONFIG.items():
        if ((backend == 'mpi') and (not mpi_available)):
            continue
        for with_init_file in {True, False}:
            tmp_dir = tempfile.mkdtemp()
            if options.verbose:
                with_init = (' with file init_method' if with_init_file else '')
                print_to_stderr('Running distributed tests for the {} backend{}'.format(backend, with_init))
            os.environ['TEMP_DIR'] = tmp_dir
            os.environ['BACKEND'] = backend
            os.environ['INIT_METHOD'] = 'env://'
            os.environ.update(env_vars)
            if with_init_file:
                init_method = 'file://{}/shared_init_file'.format(tmp_dir)
                os.environ['INIT_METHOD'] = init_method
            try:
                os.mkdir(os.path.join(tmp_dir, 'barrier'))
                os.mkdir(os.path.join(tmp_dir, 'test_dir'))
                if (backend == 'mpi'):
                    mpiexec = 'mpiexec -n 3 --noprefix {}'.format(python)
                    return_code = run_test(mpiexec, test_module, test_directory, options)
                else:
                    return_code = run_test(python, test_module, test_directory, options)
                if (return_code != 0):
                    return return_code
            finally:
                shutil.rmtree(tmp_dir)
    return 0