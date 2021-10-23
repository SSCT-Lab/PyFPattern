

@expose('/landing_times')
@has_dag_access(can_dag_read=True)
@has_access
@action_logging
@provide_session
def landing_times(self, session=None):
    default_dag_run = conf.getint('webserver', 'default_dag_run_display_number')
    dag_id = request.args.get('dag_id')
    dag = dagbag.get_dag(dag_id)
    base_date = request.args.get('base_date')
    num_runs = request.args.get('num_runs')
    num_runs = (int(num_runs) if num_runs else default_dag_run)
    if base_date:
        base_date = pendulum.parse(base_date)
    else:
        base_date = (dag.latest_execution_date or timezone.utcnow())
    dates = dag.date_range(base_date, num=(- abs(num_runs)))
    min_date = (dates[0] if dates else timezone.utc_epoch())
    root = request.args.get('root')
    if root:
        dag = dag.sub_dag(task_regex=root, include_upstream=True, include_downstream=False)
    chart_height = wwwutils.get_chart_height(dag)
    chart = nvd3.lineChart(name='lineChart', x_is_date=True, height=chart_height, width='1200')
    y = {
        
    }
    x = {
        
    }
    for task in dag.tasks:
        task_id = task.task_id
        y[task_id] = []
        x[task_id] = []
        for ti in task.get_task_instances(start_date=min_date, end_date=base_date):
            ts = ti.execution_date
            if (dag.schedule_interval and dag.following_schedule(ts)):
                ts = dag.following_schedule(ts)
            if ti.end_date:
                dttm = wwwutils.epoch(ti.execution_date)
                secs = (ti.end_date - ts).total_seconds()
                x[task_id].append(dttm)
                y[task_id].append(secs)
    y_unit = infer_time_unit([d for t in y.values() for d in t])
    chart.create_y_axis('yAxis', format='.02f', custom_format=False, label='Landing Time ({})'.format(y_unit))
    chart.axislist['yAxis']['axisLabelDistance'] = '40'
    for task in dag.tasks:
        if x[task.task_id]:
            chart.add_serie(name=task.task_id, x=x[task.task_id], y=scale_time_units(y[task.task_id], y_unit))
    tis = dag.get_task_instances(start_date=min_date, end_date=base_date)
    dates = sorted(list({ti.execution_date for ti in tis}))
    max_date = (max([ti.execution_date for ti in tis]) if dates else None)
    session.commit()
    form = DateTimeWithNumRunsForm(data={
        'base_date': max_date,
        'num_runs': num_runs,
    })
    chart.buildcontent()
    return self.render_template('airflow/chart.html', dag=dag, chart=chart.htmlcontent, height=(str((chart_height + 100)) + 'px'), demo_mode=conf.getboolean('webserver', 'demo_mode'), root=root, form=form)
