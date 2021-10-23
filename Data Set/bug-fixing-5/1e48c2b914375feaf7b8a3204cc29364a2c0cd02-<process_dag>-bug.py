def process_dag(self, dag, queue):
    '\n        This method schedules a single DAG by looking at the latest\n        run for each task and attempting to schedule the following run.\n\n        As multiple schedulers may be running for redundancy, this\n        function takes a lock on the DAG and timestamps the last run\n        in ``last_scheduler_run``.\n        '
    DagModel = models.DagModel
    session = settings.Session()
    pickle_id = None
    if (self.do_pickle and (self.executor.__class__ not in (executors.LocalExecutor, executors.SequentialExecutor))):
        pickle_id = dag.pickle(session).id
    db_dag = session.query(DagModel).filter_by(dag_id=dag.dag_id).with_for_update().one()
    last_scheduler_run = (db_dag.last_scheduler_run or datetime(2000, 1, 1))
    secs_since_last = (datetime.now() - last_scheduler_run).total_seconds()
    if (secs_since_last < self.heartrate):
        session.commit()
        session.close()
        return None
    db_dag.last_scheduler_run = datetime.now()
    session.commit()
    dag_runs = DagRun.find(dag_id=dag.dag_id, state=State.RUNNING)
    active_dag_runs = []
    for run in dag_runs:
        if (run.execution_date > datetime.now()):
            continue
        run.dag = dag
        run.verify_integrity()
        run.update_state()
        if (run.state == State.RUNNING):
            active_dag_runs.append(run)
    for run in active_dag_runs:
        tis = run.get_task_instances(session=session, state=(State.NONE, State.UP_FOR_RETRY))
        for ti in tis:
            task = dag.get_task(ti.task_id)
            ti.task = task
            if task.adhoc:
                continue
            if ti.is_runnable(flag_upstream_failed=True):
                self.logger.debug('Queuing task: {}'.format(ti))
                ti.refresh_from_db(session=session, lock_for_update=True)
                if (ti.state is State.SCHEDULED):
                    session.commit()
                    self.logger.debug('Task {} was picked up by another scheduler'.format(ti))
                    continue
                elif (ti.state is State.NONE):
                    ti.state = State.SCHEDULED
                    session.merge(ti)
                session.commit()
                queue.put((ti.key, pickle_id))
    session.close()