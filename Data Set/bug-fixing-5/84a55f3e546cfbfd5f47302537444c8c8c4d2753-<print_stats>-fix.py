def print_stats(self):
    '\n        Print operational metrics for the scheduler test.\n        '
    session = settings.Session()
    TI = TaskInstance
    tis = session.query(TI).filter(TI.dag_id.in_(DAG_IDS)).all()
    successful_tis = [x for x in tis if (x.state == State.SUCCESS)]
    ti_perf = [(ti.dag_id, ti.task_id, ti.execution_date, (ti.queued_dttm - self.start_date).total_seconds(), (ti.start_date - self.start_date).total_seconds(), (ti.end_date - self.start_date).total_seconds(), ti.duration) for ti in successful_tis]
    ti_perf_df = pd.DataFrame(ti_perf, columns=['dag_id', 'task_id', 'execution_date', 'queue_delay', 'start_delay', 'land_time', 'duration'])
    print('Performance Results')
    print('###################')
    for dag_id in DAG_IDS:
        print('DAG {}'.format(dag_id))
        print(ti_perf_df[(ti_perf_df['dag_id'] == dag_id)])
    print('###################')
    if (len(tis) > len(successful_tis)):
        print("WARNING!! The following task instances haven't completed")
        print(pd.DataFrame([(ti.dag_id, ti.task_id, ti.execution_date, ti.state) for ti in filter((lambda x: (x.state != State.SUCCESS)), tis)], columns=['dag_id', 'task_id', 'execution_date', 'state']))
    session.commit()