

@provide_session
def set_state(task, execution_date, upstream=False, downstream=False, future=False, past=False, state=State.SUCCESS, commit=False, session=None):
    '\n    Set the state of a task instance and if needed its relatives. Can set state\n    for future tasks (calculated from execution_date) and retroactively\n    for past tasks. Will verify integrity of past dag runs in order to create\n    tasks that did not exist. It will not create dag runs that are missing\n    on the schedule (but it will as for subdag dag runs if needed).\n    :param task: the task from which to work. task.task.dag needs to be set\n    :param execution_date: the execution date from which to start looking\n    :param upstream: Mark all parents (upstream tasks)\n    :param downstream: Mark all siblings (downstream tasks) of task_id, including SubDags\n    :param future: Mark all future tasks on the interval of the dag up until\n        last execution date.\n    :param past: Retroactively mark all tasks starting from start_date of the DAG\n    :param state: State to which the tasks need to be set\n    :param commit: Commit tasks to be altered to the database\n    :param session: database session\n    :return: list of tasks that have been created and updated\n    '
    assert timezone.is_localized(execution_date)
    execution_date = execution_date.replace(microsecond=0)
    assert (task.dag is not None)
    dag = task.dag
    latest_execution_date = dag.latest_execution_date
    assert (latest_execution_date is not None)
    end_date = (latest_execution_date if future else execution_date)
    if ('start_date' in dag.default_args):
        start_date = dag.default_args['start_date']
    elif dag.start_date:
        start_date = dag.start_date
    else:
        start_date = execution_date
    start_date = (execution_date if (not past) else start_date)
    if (dag.schedule_interval == '@once'):
        dates = [start_date]
    else:
        dates = dag.date_range(start_date=start_date, end_date=end_date)
    task_ids = [task.task_id]
    if downstream:
        relatives = task.get_flat_relatives(upstream=False)
        task_ids += [t.task_id for t in relatives]
    if upstream:
        relatives = task.get_flat_relatives(upstream=True)
        task_ids += [t.task_id for t in relatives]
    confirmed_dates = []
    drs = DagRun.find(dag_id=dag.dag_id, execution_date=dates)
    for dr in drs:
        dr.dag = dag
        dr.verify_integrity()
        confirmed_dates.append(dr.execution_date)
    dags = [dag]
    sub_dag_ids = []
    while (len(dags) > 0):
        current_dag = dags.pop()
        for task_id in task_ids:
            if (not current_dag.has_task(task_id)):
                continue
            current_task = current_dag.get_task(task_id)
            if isinstance(current_task, SubDagOperator):
                drs = _create_dagruns(current_task.subdag, execution_dates=confirmed_dates, state=State.RUNNING, run_id_template=BackfillJob.ID_FORMAT_PREFIX)
                for dr in drs:
                    dr.dag = current_task.subdag
                    dr.verify_integrity()
                    if commit:
                        dr.state = state
                        session.merge(dr)
                dags.append(current_task.subdag)
                sub_dag_ids.append(current_task.subdag.dag_id)
    TI = TaskInstance
    qry_dag = session.query(TI).filter((TI.dag_id == dag.dag_id), TI.execution_date.in_(confirmed_dates), TI.task_id.in_(task_ids)).filter(or_(TI.state.is_(None), (TI.state != state)))
    if (len(sub_dag_ids) > 0):
        qry_sub_dag = session.query(TI).filter(TI.dag_id.in_(sub_dag_ids), TI.execution_date.in_(confirmed_dates)).filter(or_(TI.state.is_(None), (TI.state != state)))
    if commit:
        tis_altered = qry_dag.with_for_update().all()
        if (len(sub_dag_ids) > 0):
            tis_altered += qry_sub_dag.with_for_update().all()
        for ti in tis_altered:
            ti.state = state
    else:
        tis_altered = qry_dag.all()
        if (len(sub_dag_ids) > 0):
            tis_altered += qry_sub_dag.all()
    return tis_altered
