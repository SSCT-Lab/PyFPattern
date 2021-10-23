@provide_session
def _change_state_for_tis_without_dagrun(self, simple_dag_bag, old_states, new_state, session=None):
    '\n        For all DAG IDs in the SimpleDagBag, look for task instances in the\n        old_states and set them to new_state if the corresponding DagRun\n        does not exist or exists but is not in the running state. This\n        normally should not happen, but it can if the state of DagRuns are\n        changed manually.\n\n        :param old_states: examine TaskInstances in this state\n        :type old_state: list[airflow.utils.state.State]\n        :param new_state: set TaskInstances to this state\n        :type new_state: airflow.utils.state.State\n        :param simple_dag_bag: TaskInstances associated with DAGs in the\n            simple_dag_bag and with states in the old_state will be examined\n        :type simple_dag_bag: airflow.utils.dag_processing.SimpleDagBag\n        '
    tis_changed = 0
    query = session.query(models.TaskInstance).outerjoin(models.DagRun, and_((models.TaskInstance.dag_id == models.DagRun.dag_id), (models.TaskInstance.execution_date == models.DagRun.execution_date))).filter(models.TaskInstance.dag_id.in_(simple_dag_bag.dag_ids)).filter(models.TaskInstance.state.in_(old_states)).filter(or_((models.DagRun.state != State.RUNNING), models.DagRun.state.is_(None)))
    if self.using_sqlite:
        tis_to_change = query.with_for_update().all()
        for ti in tis_to_change:
            ti.set_state(new_state, session=session)
            tis_changed += 1
    else:
        subq = query.subquery()
        tis_changed = session.query(models.TaskInstance).filter(and_((models.TaskInstance.dag_id == subq.c.dag_id), (models.TaskInstance.task_id == subq.c.task_id), (models.TaskInstance.execution_date == subq.c.execution_date))).update({
            models.TaskInstance.state: new_state,
        }, synchronize_session=False)
        session.commit()
    if (tis_changed > 0):
        self.log.warning('Set %s task instances to state=%s as their associated DagRun was not in RUNNING state', tis_changed, new_state)
        Stats.gauge('scheduler.tasks.without_dagrun', tis_changed)