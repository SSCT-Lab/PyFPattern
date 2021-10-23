@cli_utils.action_logging
def list_dag_runs(args, dag=None):
    'Lists dag runs for a given DAG'
    if dag:
        args.dag_id = dag.dag_id
    dagbag = DagBag()
    if (args.dag_id not in dagbag.dags):
        error_message = 'Dag id {} not found'.format(args.dag_id)
        raise AirflowException(error_message)
    dag_runs = list()
    state = (args.state.lower() if args.state else None)
    for dag_run in DagRun.find(dag_id=args.dag_id, state=state, no_backfills=args.no_backfill):
        dag_runs.append({
            'id': dag_run.id,
            'run_id': dag_run.run_id,
            'state': dag_run.state,
            'dag_id': dag_run.dag_id,
            'execution_date': dag_run.execution_date.isoformat(),
            'start_date': ((dag_run.start_date or '') and dag_run.start_date.isoformat()),
        })
    if (not dag_runs):
        print('No dag runs for {dag_id}'.format(dag_id=args.dag_id))
    header_template = textwrap.dedent('\n\n    {line}\n    DAG RUNS\n    {line}\n    {dag_run_header}\n    ')
    dag_runs.sort(key=(lambda x: x['execution_date']), reverse=True)
    dag_run_header = ('%-3s | %-20s | %-10s | %-20s | %-20s |' % ('id', 'run_id', 'state', 'execution_date', 'state_date'))
    print(header_template.format(dag_run_header=dag_run_header, line=('-' * 120)))
    for dag_run in dag_runs:
        record = ('%-3s | %-20s | %-10s | %-20s | %-20s |' % (dag_run['id'], dag_run['run_id'], dag_run['state'], dag_run['execution_date'], dag_run['start_date']))
        print(record)