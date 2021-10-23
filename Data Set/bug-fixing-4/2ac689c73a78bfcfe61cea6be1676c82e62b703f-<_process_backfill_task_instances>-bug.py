@provide_session
def _process_backfill_task_instances(self, ti_status, executor, pickle_id, start_date=None, session=None):
    '\n        Process a set of task instances from a set of dag runs. Special handling is done\n        to account for different task instance states that could be present when running\n        them in a backfill process.\n\n        :param ti_status: the internal status of the job\n        :type ti_status: BackfillJob._DagRunTaskStatus\n        :param executor: the executor to run the task instances\n        :type executor: BaseExecutor\n        :param pickle_id: the pickle_id if dag is pickled, None otherwise\n        :type pickle_id: int\n        :param start_date: the start date of the backfill job\n        :type start_date: datetime.datetime\n        :param session: the current session object\n        :type session: sqlalchemy.orm.session.Session\n        :return: the list of execution_dates for the finished dag runs\n        :rtype: list\n        '
    executed_run_dates = []
    while (((len(ti_status.to_run) > 0) or (len(ti_status.running) > 0)) and (len(ti_status.deadlocked) == 0)):
        self.log.debug('*** Clearing out not_ready list ***')
        ti_status.not_ready.clear()
        for task in self.dag.topological_sort():
            for (key, ti) in list(ti_status.to_run.items()):
                if (task.task_id != ti.task_id):
                    continue
                ti.refresh_from_db()
                task = self.dag.get_task(ti.task_id)
                ti.task = task
                ignore_depends_on_past = (self.ignore_first_depends_on_past and (ti.execution_date == (start_date or ti.start_date)))
                self.log.debug('Task instance to run %s state %s', ti, ti.state)
                if (ti.state == State.SUCCESS):
                    ti_status.succeeded.add(key)
                    self.log.debug("Task instance %s succeeded. Don't rerun.", ti)
                    ti_status.to_run.pop(key)
                    if (key in ti_status.running):
                        ti_status.running.pop(key)
                    continue
                elif (ti.state == State.SKIPPED):
                    ti_status.skipped.add(key)
                    self.log.debug("Task instance %s skipped. Don't rerun.", ti)
                    ti_status.to_run.pop(key)
                    if (key in ti_status.running):
                        ti_status.running.pop(key)
                    continue
                elif (ti.state == State.NONE):
                    self.log.warning('FIXME: task instance {} state was set to None externally. This should not happen')
                    ti.set_state(State.SCHEDULED, session=session)
                if self.rerun_failed_tasks:
                    if (ti.state in (State.FAILED, State.UPSTREAM_FAILED)):
                        self.log.error('Task instance {ti} with state {state}'.format(ti=ti, state=ti.state))
                        if (key in ti_status.running):
                            ti_status.running.pop(key)
                        ti.set_state(State.SCHEDULED, session=session)
                elif (ti.state in (State.FAILED, State.UPSTREAM_FAILED)):
                    self.log.error('Task instance {ti} with {state} state'.format(ti=ti, state=ti.state))
                    ti_status.failed.add(key)
                    ti_status.to_run.pop(key)
                    if (key in ti_status.running):
                        ti_status.running.pop(key)
                    continue
                backfill_context = DepContext(deps=RUN_DEPS, ignore_depends_on_past=ignore_depends_on_past, ignore_task_deps=self.ignore_task_deps, flag_upstream_failed=True)
                if ti.are_dependencies_met(dep_context=backfill_context, session=session, verbose=self.verbose):
                    ti.refresh_from_db(lock_for_update=True, session=session)
                    if (ti.state in (State.SCHEDULED, State.UP_FOR_RETRY, State.UP_FOR_RESCHEDULE)):
                        if executor.has_task(ti):
                            self.log.debug('Task Instance %s already in executor waiting for queue to clear', ti)
                        else:
                            self.log.debug('Sending %s to executor', ti)
                            ti.state = State.QUEUED
                            ti.queued_dttm = (timezone.utcnow() if (not ti.queued_dttm) else ti.queued_dttm)
                            session.merge(ti)
                            cfg_path = None
                            if (executor.__class__ in (executors.LocalExecutor, executors.SequentialExecutor)):
                                cfg_path = tmp_configuration_copy()
                            executor.queue_task_instance(ti, mark_success=self.mark_success, pickle_id=pickle_id, ignore_task_deps=self.ignore_task_deps, ignore_depends_on_past=ignore_depends_on_past, pool=self.pool, cfg_path=cfg_path)
                            ti_status.running[key] = ti
                            ti_status.to_run.pop(key)
                    session.commit()
                    continue
                if (ti.state == State.UPSTREAM_FAILED):
                    self.log.error('Task instance %s upstream failed', ti)
                    ti_status.failed.add(key)
                    ti_status.to_run.pop(key)
                    if (key in ti_status.running):
                        ti_status.running.pop(key)
                    continue
                if (ti.state == State.UP_FOR_RETRY):
                    self.log.debug('Task instance %s retry period not expired yet', ti)
                    if (key in ti_status.running):
                        ti_status.running.pop(key)
                    ti_status.to_run[key] = ti
                    continue
                if (ti.state == State.UP_FOR_RESCHEDULE):
                    self.log.debug('Task instance %s reschedule period not expired yet', ti)
                    if (key in ti_status.running):
                        ti_status.running.pop(key)
                    ti_status.to_run[key] = ti
                    continue
                self.log.debug('Adding %s to not_ready', ti)
                ti_status.not_ready.add(key)
        self.heartbeat()
        executor.heartbeat()
        if (ti_status.not_ready and (ti_status.not_ready == set(ti_status.to_run)) and (len(ti_status.running) == 0)):
            self.log.warning('Deadlock discovered for ti_status.to_run=%s', ti_status.to_run.values())
            ti_status.deadlocked.update(ti_status.to_run.values())
            ti_status.to_run.clear()
        self._manage_executor_state(ti_status.running)
        self._update_counters(ti_status=ti_status)
        _dag_runs = ti_status.active_runs[:]
        for run in _dag_runs:
            run.update_state(session=session)
            if (run.state in State.finished()):
                ti_status.finished_runs += 1
                ti_status.active_runs.remove(run)
                executed_run_dates.append(run.execution_date)
        self._log_progress(ti_status)
    return executed_run_dates