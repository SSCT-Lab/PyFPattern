@provide_session
def manage_slas(self, dag, session=None):
    '\n        Finding all tasks that have SLAs defined, and sending alert emails\n        where needed. New SLA misses are also recorded in the database.\n\n        Where assuming that the scheduler runs often, so we only check for\n        tasks that should have succeeded in the past hour.\n        '
    if (not any([isinstance(ti.sla, timedelta) for ti in dag.tasks])):
        self.log.info('Skipping SLA check for %s because no tasks in DAG have SLAs', dag)
        return
    if (dag._schedule_interval is None):
        self.log.info("SLA check for DAGs with schedule_interval 'None'/'@once' are skipped in 1.10.4, due to related refactoring going on.")
        return
    TI = models.TaskInstance
    sq = session.query(TI.task_id, func.max(TI.execution_date).label('max_ti')).with_hint(TI, 'USE INDEX (PRIMARY)', dialect_name='mysql').filter((TI.dag_id == dag.dag_id)).filter(or_((TI.state == State.SUCCESS), (TI.state == State.SKIPPED))).filter(TI.task_id.in_(dag.task_ids)).group_by(TI.task_id).subquery('sq')
    max_tis = session.query(TI).filter((TI.dag_id == dag.dag_id), (TI.task_id == sq.c.task_id), (TI.execution_date == sq.c.max_ti)).all()
    ts = timezone.utcnow()
    for ti in max_tis:
        task = dag.get_task(ti.task_id)
        dttm = ti.execution_date
        if isinstance(task.sla, timedelta):
            dttm = dag.following_schedule(dttm)
            while (dttm < timezone.utcnow()):
                following_schedule = dag.following_schedule(dttm)
                if ((following_schedule + task.sla) < timezone.utcnow()):
                    session.merge(SlaMiss(task_id=ti.task_id, dag_id=ti.dag_id, execution_date=dttm, timestamp=ts))
                dttm = dag.following_schedule(dttm)
    session.commit()
    slas = session.query(SlaMiss).filter((SlaMiss.notification_sent == False), (SlaMiss.dag_id == dag.dag_id)).all()
    if slas:
        sla_dates = [sla.execution_date for sla in slas]
        qry = session.query(TI).filter((TI.state != State.SUCCESS), TI.execution_date.in_(sla_dates), (TI.dag_id == dag.dag_id)).all()
        blocking_tis = []
        for ti in qry:
            if (ti.task_id in dag.task_ids):
                ti.task = dag.get_task(ti.task_id)
                blocking_tis.append(ti)
            else:
                session.delete(ti)
                session.commit()
        task_list = '\n'.join([((sla.task_id + ' on ') + sla.execution_date.isoformat()) for sla in slas])
        blocking_task_list = '\n'.join([((ti.task_id + ' on ') + ti.execution_date.isoformat()) for ti in blocking_tis])
        email_sent = False
        notification_sent = False
        if dag.sla_miss_callback:
            self.log.info(' --------------> ABOUT TO CALL SLA MISS CALL BACK ')
            try:
                dag.sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis)
                notification_sent = True
            except Exception:
                self.log.exception('Could not call sla_miss_callback for DAG %s', dag.dag_id)
        email_content = "            Here's a list of tasks that missed their SLAs:\n            <pre><code>{task_list}\n<code></pre>\n            Blocking tasks:\n            <pre><code>{blocking_task_list}\n{bug}<code></pre>\n            ".format(task_list=task_list, blocking_task_list=blocking_task_list, bug=asciiart.bug)
        emails = set()
        for task in dag.tasks:
            if task.email:
                if isinstance(task.email, basestring):
                    emails |= set(get_email_address_list(task.email))
                elif isinstance(task.email, (list, tuple)):
                    emails |= set(task.email)
        if emails:
            try:
                send_email(emails, ('[airflow] SLA miss on DAG=' + dag.dag_id), email_content)
                email_sent = True
                notification_sent = True
            except Exception:
                self.log.exception('Could not send SLA Miss email notification for DAG %s', dag.dag_id)
        if notification_sent:
            for sla in slas:
                if email_sent:
                    sla.email_sent = True
                sla.notification_sent = True
                session.merge(sla)
        session.commit()