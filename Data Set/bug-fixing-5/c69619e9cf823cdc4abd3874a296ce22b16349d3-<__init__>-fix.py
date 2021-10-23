def __init__(self, conf=None, conn_id='spark_default', files=None, py_files=None, driver_classpath=None, jars=None, java_class=None, packages=None, exclude_packages=None, repositories=None, total_executor_cores=None, executor_cores=None, executor_memory=None, driver_memory=None, keytab=None, principal=None, name='default-name', num_executors=None, application_args=None, env_vars=None, verbose=False, spark_binary='spark-submit'):
    self._conf = conf
    self._conn_id = conn_id
    self._files = files
    self._py_files = py_files
    self._driver_classpath = driver_classpath
    self._jars = jars
    self._java_class = java_class
    self._packages = packages
    self._exclude_packages = exclude_packages
    self._repositories = repositories
    self._total_executor_cores = total_executor_cores
    self._executor_cores = executor_cores
    self._executor_memory = executor_memory
    self._driver_memory = driver_memory
    self._keytab = keytab
    self._principal = principal
    self._name = name
    self._num_executors = num_executors
    self._application_args = application_args
    self._env_vars = env_vars
    self._verbose = verbose
    self._submit_sp = None
    self._yarn_application_id = None
    self._kubernetes_driver_pod = None
    self._spark_binary = spark_binary
    self._connection = self._resolve_connection()
    self._is_yarn = ('yarn' in self._connection['master'])
    self._is_kubernetes = ('k8s' in self._connection['master'])
    if (self._is_kubernetes and (kube_client is None)):
        raise RuntimeError('{} specified by kubernetes dependencies are not installed!'.format(self._connection['master']))
    self._should_track_driver_status = self._resolve_should_track_driver_status()
    self._driver_id = None
    self._driver_status = None
    self._spark_exit_code = None