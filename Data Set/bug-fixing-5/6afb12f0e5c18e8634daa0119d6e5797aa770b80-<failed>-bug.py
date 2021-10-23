@expose('/failed', methods=['POST'])
@has_dag_access(can_dag_edit=True)
@has_access
@action_logging
def failed(self):
    dag_id = request.form.get('dag_id')
    task_id = request.form.get('task_id')
    origin = request.form.get('origin')
    execution_date = request.form.get('execution_date')
    confirmed = (request.form.get('confirmed') == 'true')
    upstream = (request.form.get('upstream') == 'true')
    downstream = (request.form.get('downstream') == 'true')
    future = (request.form.get('future') == 'true')
    past = (request.form.get('past') == 'true')
    return self._mark_task_instance_state(dag_id, task_id, origin, execution_date, confirmed, upstream, downstream, future, past, State.FAILED)