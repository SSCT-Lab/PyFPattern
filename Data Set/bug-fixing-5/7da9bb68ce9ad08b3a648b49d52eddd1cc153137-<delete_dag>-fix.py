def delete_dag(dag_id, keep_records_in_log=True):
    '\n    :param dag_id: the dag_id of the DAG to delete\n    :type dag_id: str\n    :param keep_records_in_log: whether keep records of the given dag_id\n        in the Log table in the backend database (for reasons like auditing).\n        The default value is True.\n    :type keep_records_in_log: bool\n    '
    session = settings.Session()
    DM = models.DagModel
    dag = session.query(DM).filter((DM.dag_id == dag_id)).first()
    if (dag is None):
        raise DagNotFound('Dag id {} not found'.format(dag_id))
    if (dag.fileloc and os.path.exists(dag.fileloc)):
        raise DagFileExists('Dag id {} is still in DagBag. Remove the DAG file first: {}'.format(dag_id, dag.fileloc))
    count = 0
    for m in models.base.Base._decl_class_registry.values():
        if hasattr(m, 'dag_id'):
            if (keep_records_in_log and (m.__name__ == 'Log')):
                continue
            cond = or_((m.dag_id == dag_id), m.dag_id.like((dag_id + '.%')))
            count += session.query(m).filter(cond).delete(synchronize_session='fetch')
    if dag.is_subdag:
        (p, c) = dag_id.rsplit('.', 1)
        for m in (models.DagRun, models.TaskFail, models.TaskInstance):
            count += session.query(m).filter((m.dag_id == p), (m.task_id == c)).delete()
    session.commit()
    return count