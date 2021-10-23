def heartbeat(self):
    '\n        Override the scheduler heartbeat to determine when the test is complete\n        '
    super(SchedulerMetricsJob, self).heartbeat()
    session = settings.Session()
    TI = TaskInstance
    successful_tis = session.query(TI).filter(TI.dag_id.in_(DAG_IDS)).filter(TI.state.in_([State.SUCCESS])).all()
    session.commit()
    dagbag = DagBag(SUBDIR)
    dags = [dagbag.dags[dag_id] for dag_id in DAG_IDS]
    num_task_instances = sum([(timezone.utcnow() - task.start_date).days for dag in dags for task in dag.tasks])
    if ((len(successful_tis) == num_task_instances) or ((timezone.utcnow() - self.start_date).total_seconds() > MAX_RUNTIME_SECS)):
        if (len(successful_tis) == num_task_instances):
            self.log.info('All tasks processed! Printing stats.')
        else:
            self.log.info('Test timeout reached. Printing available stats.')
        self.print_stats()
        set_dags_paused_state(True)
        sys.exit()