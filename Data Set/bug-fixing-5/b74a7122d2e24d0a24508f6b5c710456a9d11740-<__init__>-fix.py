@provide_session
@apply_defaults
def __init__(self, subdag, executor=SequentialExecutor(), *args, **kwargs):
    import airflow.models
    dag = (kwargs.get('dag') or airflow.models._CONTEXT_MANAGER_DAG)
    if (not dag):
        raise AirflowException('Please pass in the `dag` param or call within a DAG context manager')
    session = kwargs.pop('session')
    super(SubDagOperator, self).__init__(*args, **kwargs)
    if (((dag.dag_id + '.') + kwargs['task_id']) != subdag.dag_id):
        raise AirflowException("The subdag's dag_id should have the form '{{parent_dag_id}}.{{this_task_id}}'. Expected '{d}.{t}'; received '{rcvd}'.".format(d=dag.dag_id, t=kwargs['task_id'], rcvd=subdag.dag_id))
    if self.pool:
        conflicts = [t for t in subdag.tasks if (t.pool == self.pool)]
        if conflicts:
            pool = session.query(Pool).filter((Pool.slots == 1)).filter((Pool.pool == self.pool)).first()
            if (pool and any(((t.pool == self.pool) for t in subdag.tasks))):
                raise AirflowException('SubDagOperator {sd} and subdag task{plural} {t} both use pool {p}, but the pool only has 1 slot. The subdag tasks will never run.'.format(sd=self.task_id, plural=(len(conflicts) > 1), t=', '.join((t.task_id for t in conflicts)), p=self.pool))
    self.subdag = subdag
    self.executor = executor