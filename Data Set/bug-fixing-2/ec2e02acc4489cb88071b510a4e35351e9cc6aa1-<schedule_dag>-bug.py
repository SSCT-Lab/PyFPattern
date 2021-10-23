

def schedule_dag(self, dag):
    '\n        This method checks whether a new DagRun needs to be created\n        for a DAG based on scheduling interval\n        Returns DagRun if one is scheduled. Otherwise returns None.\n        '
    if dag.schedule_interval:
        DagRun = models.DagRun
        session = settings.Session()
        qry = session.query(DagRun).filter((DagRun.dag_id == dag.dag_id), (DagRun.external_trigger == False), (DagRun.state == State.RUNNING))
        active_runs = qry.all()
        if (len(active_runs) >= dag.max_active_runs):
            return
        for dr in active_runs:
            if (dr.start_date and dag.dagrun_timeout and (dr.start_date < (datetime.now() - dag.dagrun_timeout))):
                dr.state = State.FAILED
                dr.end_date = datetime.now()
        session.commit()
        qry = session.query(func.max(DagRun.execution_date)).filter_by(dag_id=dag.dag_id).filter(or_((DagRun.external_trigger == False), DagRun.run_id.like((DagRun.ID_PREFIX + '%'))))
        last_scheduled_run = qry.scalar()
        next_run_date = None
        if (not last_scheduled_run):
            TI = models.TaskInstance
            latest_run = session.query(func.max(TI.execution_date)).filter_by(dag_id=dag.dag_id).scalar()
            if latest_run:
                next_run_date = dag.date_range(latest_run, (- 5))[0]
            else:
                next_run_date = min([t.start_date for t in dag.tasks])
        elif (dag.schedule_interval != '@once'):
            next_run_date = dag.following_schedule(last_scheduled_run)
        elif ((dag.schedule_interval == '@once') and (not last_scheduled_run)):
            next_run_date = datetime.now()
        if (dag.schedule_interval == '@once'):
            schedule_end = next_run_date
        elif next_run_date:
            schedule_end = dag.following_schedule(next_run_date)
        if (next_run_date and dag.end_date and (next_run_date > dag.end_date)):
            return
        if (next_run_date and schedule_end and (schedule_end <= datetime.now())):
            next_run = DagRun(dag_id=dag.dag_id, run_id=('scheduled__' + next_run_date.isoformat()), execution_date=next_run_date, start_date=datetime.now(), state=State.RUNNING, external_trigger=False)
            session.add(next_run)
            session.commit()
            return next_run
