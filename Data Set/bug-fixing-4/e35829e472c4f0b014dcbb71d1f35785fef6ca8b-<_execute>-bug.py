def _execute(self):
    self.log.info('Starting the scheduler')
    pickle_dags = False
    if (self.do_pickle and (self.executor.__class__ not in (executors.LocalExecutor, executors.SequentialExecutor))):
        pickle_dags = True
    self.log.info('Processing each file at most %s times', self.num_runs)
    self.log.info('Searching for files in %s', self.subdir)
    known_file_paths = list_py_file_paths(self.subdir)
    self.log.info('There are %s files in %s', len(known_file_paths), self.subdir)

    def processor_factory(file_path, zombies):
        return DagFileProcessor(file_path, pickle_dags, self.dag_ids, zombies)
    async_mode = (not self.using_sqlite)
    processor_timeout_seconds = conf.getint('core', 'dag_file_processor_timeout')
    processor_timeout = timedelta(seconds=processor_timeout_seconds)
    self.processor_agent = DagFileProcessorAgent(self.subdir, known_file_paths, self.num_runs, processor_factory, processor_timeout, async_mode)
    try:
        self.log.debug('Starting executor=%s', self.executor)
        self.executor.start()
        self._execute_helper()
    except Exception:
        self.log.exception('Exception when executing execute_helper')
    finally:
        self.log.debug('Calling executor.end()...')
        self.executor.end()
        self.processor_agent.end()
        self.log.debug('Calling settings.Session.remove()...')
        settings.Session.remove()
        self.log.info('Exited execute loop')