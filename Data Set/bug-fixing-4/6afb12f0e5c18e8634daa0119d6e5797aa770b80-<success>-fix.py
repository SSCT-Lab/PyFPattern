@expose('/success', methods=['POST'])
@has_dag_access(can_dag_edit=True)
@has_access
@action_logging
def success(self):
    dag_id = request.form.get('dag_id')
    task_id = request.form.get('task_id')
    origin = request.form.get('origin')
    execution_date = request.form.get('execution_date')
    confirmed = (request.form.get('confirmed') == 'true')
    upstream = (request.form.get('success_upstream') == 'true')
    downstream = (request.form.get('success_downstream') == 'true')
    future = (request.form.get('success_future') == 'true')
    past = (request.form.get('success_past') == 'true')
    return self._mark_task_instance_state(dag_id, task_id, origin, execution_date, confirmed, upstream, downstream, future, past, State.SUCCESS)