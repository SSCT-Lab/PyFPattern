def main():
    global MAX_RUNTIME_SECS
    if (len(sys.argv) > 1):
        try:
            max_runtime_secs = int(sys.argv[1])
            if (max_runtime_secs < 1):
                raise ValueError
            MAX_RUNTIME_SECS = max_runtime_secs
        except ValueError:
            logging.error('Specify a positive integer for timeout.')
            sys.exit(1)
    configuration.load_test_config()
    set_dags_paused_state(False)
    clear_dag_runs()
    clear_dag_task_instances()
    job = SchedulerMetricsJob(dag_ids=DAG_IDS, subdir=SUBDIR)
    job.run()