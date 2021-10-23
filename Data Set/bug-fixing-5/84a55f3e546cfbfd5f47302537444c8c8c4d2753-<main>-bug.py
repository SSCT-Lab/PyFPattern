def main():
    configuration.load_test_config()
    set_dags_paused_state(False)
    clear_dag_runs()
    clear_dag_task_instances()
    job = SchedulerMetricsJob(dag_ids=DAG_IDS, subdir=SUBDIR)
    job.run()