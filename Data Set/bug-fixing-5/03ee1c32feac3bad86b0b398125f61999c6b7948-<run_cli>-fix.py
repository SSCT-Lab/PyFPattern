def run_cli(self, hql, schema=None, verbose=True, hive_conf=None):
    '\n        Run an hql statement using the hive cli. If hive_conf is specified\n        it should be a dict and the entries will be set as key/value pairs\n        in HiveConf\n\n\n        :param hive_conf: if specified these key value pairs will be passed\n            to hive as ``-hiveconf "key"="value"``. Note that they will be\n            passed after the ``hive_cli_params`` and thus will override\n            whatever values are specified in the database.\n        :type hive_conf: dict\n\n        >>> hh = HiveCliHook()\n        >>> result = hh.run_cli("USE airflow;")\n        >>> ("OK" in result)\n        True\n        '
    conn = self.conn
    schema = (schema or conn.schema)
    if schema:
        hql = 'USE {schema};\n{hql}'.format(schema=schema, hql=hql)
    with TemporaryDirectory(prefix='airflow_hiveop_') as tmp_dir:
        with NamedTemporaryFile(dir=tmp_dir) as f:
            hql = (hql + '\n')
            f.write(hql.encode('UTF-8'))
            f.flush()
            hive_cmd = self._prepare_cli_cmd()
            env_context = get_context_from_env_var()
            if hive_conf:
                env_context.update(hive_conf)
            hive_conf_params = self._prepare_hiveconf(env_context)
            if self.mapred_queue:
                hive_conf_params.extend(['-hiveconf', 'mapreduce.job.queuename={}'.format(self.mapred_queue), '-hiveconf', 'mapred.job.queue.name={}'.format(self.mapred_queue), '-hiveconf', 'tez.queue.name={}'.format(self.mapred_queue)])
            if self.mapred_queue_priority:
                hive_conf_params.extend(['-hiveconf', 'mapreduce.job.priority={}'.format(self.mapred_queue_priority)])
            if self.mapred_job_name:
                hive_conf_params.extend(['-hiveconf', 'mapred.job.name={}'.format(self.mapred_job_name)])
            hive_cmd.extend(hive_conf_params)
            hive_cmd.extend(['-f', f.name])
            if verbose:
                self.log.info('%s', ' '.join(hive_cmd))
            sp = subprocess.Popen(hive_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=tmp_dir, close_fds=True)
            self.sp = sp
            stdout = ''
            while True:
                line = sp.stdout.readline()
                if (not line):
                    break
                stdout += line.decode('UTF-8')
                if verbose:
                    self.log.info(line.decode('UTF-8').strip())
            sp.wait()
            if sp.returncode:
                raise AirflowException(stdout)
            return stdout