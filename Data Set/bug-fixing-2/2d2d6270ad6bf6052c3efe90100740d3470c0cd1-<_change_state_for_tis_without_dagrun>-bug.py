

@provide_session
def _change_state_for_tis_without_dagrun(self, simple_dag_bag, old_states, new_state, session=None):
    '\n        For all DAG IDs in the SimpleDagBag, look for task instances in the\n        old_states and set them to new_state if the corresponding DagRun\n        exists but is not in the running state. This normally should not\n        happen, but it can if the state of DagRuns are changed manually.\n\n        :param old_states: examine TaskInstances in this state\n        :type old_state: list[State]\n        :param new_state: set TaskInstances to this state\n        :type new_state: State\n        :param simple_dag_bag: TaskInstances associated with DAGs in the\n        simple_dag_bag and with states in the old_state will be examined\n        :type simple_dag_bag: SimpleDagBag\n        '
    task_instances_to_change = session.query(models.TaskInstance).filter(models.TaskInstance.dag_id.in_(simple_dag_bag.dag_ids)).filter(models.TaskInstance.state.in_(old_states)).with_for_update().all()
    ':type: list[TaskInstance]'
    for task_instance in task_instances_to_change:
        dag_runs = DagRun.find(dag_id=task_instance.dag_id, execution_date=task_instance.execution_date)
        if (len(dag_runs) == 0):
            self.logger.warn('DagRun for %s %s does not exist', task_instance.dag_id, task_instance.execution_date)
            continue
        if (len(dag_runs) > 1):
            self.logger.warn('Multiple DagRuns found for {} {}: {}'.format(task_instance.dag_id, task_instance.execution_date, dag_runs))
        dag_is_running = True
        for dag_run in dag_runs:
            if (dag_run.state == State.RUNNING):
                dag_is_running = True
                break
        if (not dag_is_running):
            self.logger.warn('Setting {} to state={} as it does not have a DagRun in the {} state'.format(task_instance, new_state, State.RUNNING))
            task_instance.state = new_state
            session.merge(task_instance)
    session.commit()
