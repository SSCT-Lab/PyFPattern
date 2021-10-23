@pytest.fixture(autouse=True, scope='session')
def breeze_test_helper(request):
    "\n    Helper that setups Airflow testing environment. It does the same thing\n    as the old 'run-tests' script.\n    "
    if os.environ.get('SKIP_INIT_DB'):
        print('Skipping db initialization. Tests do not require database')
        return
    print(' AIRFLOW '.center(60, '='))
    home = os.environ.get('HOME')
    airflow_home = (os.environ.get('AIRFLOW_HOME') or os.path.join(home, 'airflow'))
    tests_directory = os.path.dirname(os.path.realpath(__file__))
    os.environ['AIRFLOW__CORE__DAGS_FOLDER'] = os.path.join(tests_directory, 'dags')
    os.environ['AIRFLOW__CORE__UNIT_TEST_MODE'] = 'True'
    os.environ['AWS_DEFAULT_REGION'] = (os.environ.get('AWS_DEFAULT_REGION') or 'us-east-1')
    print(f'''Home of the user: {home}
Airflow home {airflow_home}''')
    lock_file = os.path.join(airflow_home, '.airflow_db_initialised')
    if request.config.option.db_init:
        print('Initializing the DB - forced with --with-db-init switch.')
        try:
            db.initdb()
        except:
            print('Skipping db initialization because database already exists.')
        db.resetdb()
    elif (not os.path.exists(lock_file)):
        print('Initializing the DB - first time after entering the container.\nYou can force re-initialization the database by adding --with-db-init switch to run-tests.')
        try:
            db.initdb()
        except:
            print('Skipping db initialization because database already exists.')
        db.resetdb()
        with open(lock_file, 'w+'):
            pass
    else:
        print('Skipping initializing of the DB as it was initialized already.\nYou can re-initialize the database by adding --with-db-init flag when running tests.')
    kerberos = os.environ.get('KRB5_KTNAME')
    if kerberos:
        subprocess.check_call(['kinit', '-kt', kerberos, 'airflow'])