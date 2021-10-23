def test_distributed(python, test_module, test_directory, verbose):
    mpi_available = (subprocess.call('command -v mpiexec', shell=True) == 0)
    if (verbose and (not mpi_available)):
        print('MPI not available -- MPI backend tests will be skipped')
    for (backend, env_vars) in DISTRIBUTED_TESTS_CONFIG.items():
        if ((backend == 'mpi') and (not mpi_available)):
            continue
        for with_init in {True, False}:
            tmp_dir = tempfile.mkdtemp()
            with_init_message = (' with file init_method' if with_init else '')
            if verbose:
                print('Running distributed tests for the {} backend{}'.format(backend, with_init_message))
            os.environ['TEMP_DIR'] = tmp_dir
            os.environ['BACKEND'] = backend
            os.environ['INIT_METHOD'] = 'env://'
            os.environ.update(env_vars)
            if with_init:
                init_method = 'file://{}/shared_init_file'.format(tmp_dir)
                os.environ['INIT_METHOD'] = init_method
            try:
                os.mkdir(os.path.join(tmp_dir, 'barrier'))
                os.mkdir(os.path.join(tmp_dir, 'test_dir'))
                if (backend == 'mpi'):
                    mpiexec = 'mpiexec -n 3 --noprefix {}'.format(python)
                    if (not run_test(mpiexec, test_module, test_directory, verbose)):
                        return False
                elif (not run_test(python, test_module, test_directory, verbose)):
                    return False
            finally:
                shutil.rmtree(tmp_dir)
    return True