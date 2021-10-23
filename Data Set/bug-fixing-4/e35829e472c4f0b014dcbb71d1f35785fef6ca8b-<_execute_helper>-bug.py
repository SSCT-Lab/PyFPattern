def _execute_helper(self):
    '\n        The actual scheduler loop. The main steps in the loop are:\n            #. Harvest DAG parsing results through DagFileProcessorAgent\n            #. Find and queue executable tasks\n                #. Change task instance state in DB\n                #. Queue tasks in executor\n            #. Heartbeat executor\n                #. Execute queued tasks in executor asynchronously\n                #. Sync on the states of running tasks\n\n        Following is a graphic representation of these steps.\n\n        .. image:: ../docs/img/scheduler_loop.jpg\n\n        :rtype: None\n        '
    self.log.info('Resetting orphaned tasks for active dag runs')
    self.reset_state_for_orphaned_tasks()
    self.processor_agent.start()
    execute_start_time = timezone.utcnow()
    last_self_heartbeat_time = timezone.utcnow()
    while True:
        self.log.debug('Starting Loop...')
        loop_start_time = time.time()
        if self.using_sqlite:
            self.processor_agent.heartbeat()
            self.log.debug("Waiting for processors to finish since we're using sqlite")
            self.processor_agent.wait_until_finished()
        self.log.debug('Harvesting DAG parsing results')
        simple_dags = self.processor_agent.harvest_simple_dags()
        self.log.debug('Harvested {} SimpleDAGs'.format(len(simple_dags)))
        simple_dag_bag = SimpleDagBag(simple_dags)
        if (len(simple_dags) > 0):
            try:
                simple_dag_bag = SimpleDagBag(simple_dags)
                self._change_state_for_tis_without_dagrun(simple_dag_bag, [State.UP_FOR_RETRY], State.FAILED)
                self._change_state_for_tis_without_dagrun(simple_dag_bag, [State.QUEUED, State.SCHEDULED, State.UP_FOR_RESCHEDULE], State.NONE)
                self._execute_task_instances(simple_dag_bag, (State.SCHEDULED,))
            except Exception as e:
                self.log.error('Error queuing tasks')
                self.log.exception(e)
                continue
        self.log.debug('Heartbeating the executor')
        self.executor.heartbeat()
        self._change_state_for_tasks_failed_to_execute()
        self._process_executor_events(simple_dag_bag)
        time_since_last_heartbeat = (timezone.utcnow() - last_self_heartbeat_time).total_seconds()
        if (time_since_last_heartbeat > self.heartrate):
            self.log.debug('Heartbeating the scheduler')
            self.heartbeat()
            last_self_heartbeat_time = timezone.utcnow()
        is_unit_test = conf.getboolean('core', 'unit_test_mode')
        loop_end_time = time.time()
        loop_duration = (loop_end_time - loop_start_time)
        self.log.debug('Ran scheduling loop in %.2f seconds', loop_duration)
        if (not is_unit_test):
            self.log.debug('Sleeping for %.2f seconds', self._processor_poll_interval)
            time.sleep(self._processor_poll_interval)
        if self.processor_agent.done:
            self.log.info('Exiting scheduler loop as all files have been processed {} times'.format(self.num_runs))
            break
        if ((loop_duration < 1) and (not is_unit_test)):
            sleep_length = (1 - loop_duration)
            self.log.debug('Sleeping for {0:.2f} seconds to prevent excessive logging'.format(sleep_length))
            sleep(sleep_length)
    self.processor_agent.terminate()
    if self.processor_agent.all_files_processed:
        self.log.info("Deactivating DAGs that haven't been touched since %s", execute_start_time.isoformat())
        models.DAG.deactivate_stale_dags(execute_start_time)