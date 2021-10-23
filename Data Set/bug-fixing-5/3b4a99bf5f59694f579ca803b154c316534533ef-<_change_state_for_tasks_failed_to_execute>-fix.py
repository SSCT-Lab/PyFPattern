@provide_session
def _change_state_for_tasks_failed_to_execute(self, session):
    '\n        If there are tasks left over in the executor,\n        we set them back to SCHEDULED to avoid creating hanging tasks.\n\n        :param session: session for ORM operations\n        '
    if self.executor.queued_tasks:
        TI = models.TaskInstance
        filter_for_ti_state_change = [and_((TI.dag_id == dag_id), (TI.task_id == task_id), (TI.execution_date == execution_date), (TI._try_number == (try_number - 1)), (TI.state == State.QUEUED)) for (dag_id, task_id, execution_date, try_number) in self.executor.queued_tasks.keys()]
        ti_query = session.query(TI).filter(or_(*filter_for_ti_state_change))
        tis_to_set_to_scheduled = ti_query.with_for_update().all()
        if (len(tis_to_set_to_scheduled) == 0):
            session.commit()
            return
        for task_instance in tis_to_set_to_scheduled:
            task_instance.state = State.SCHEDULED
        task_instance_str = '\n\t'.join(['{}'.format(x) for x in tis_to_set_to_scheduled])
        session.commit()
        self.log.info('Set the following tasks to scheduled state:\n\t{}'.format(task_instance_str))