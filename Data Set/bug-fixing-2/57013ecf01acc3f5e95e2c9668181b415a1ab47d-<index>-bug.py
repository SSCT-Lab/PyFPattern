

@expose('/home')
@has_access
@provide_session
def index(self, session=None):
    DM = models.DagModel
    hide_paused_dags_by_default = conf.getboolean('webserver', 'hide_paused_dags_by_default')
    show_paused_arg = request.args.get('showPaused', 'None')
    default_dag_run = conf.getint('webserver', 'default_dag_run_display_number')
    num_runs = request.args.get('num_runs')
    num_runs = (int(num_runs) if num_runs else default_dag_run)

    def get_int_arg(value, default=0):
        try:
            return int(value)
        except ValueError:
            return default
    arg_current_page = request.args.get('page', '0')
    arg_search_query = request.args.get('search', None)
    dags_per_page = PAGE_SIZE
    current_page = get_int_arg(arg_current_page, default=0)
    if (show_paused_arg.strip().lower() == 'false'):
        hide_paused = True
    elif (show_paused_arg.strip().lower() == 'true'):
        hide_paused = False
    else:
        hide_paused = hide_paused_dags_by_default
    query = session.query(DM).filter((~ DM.is_subdag), DM.is_active)
    if hide_paused:
        query = query.filter((~ DM.is_paused))
    if arg_search_query:
        query = query.filter((sqla.func.lower(DM.dag_id) == arg_search_query.lower()))
    import_errors = session.query(errors.ImportError).all()
    for ie in import_errors:
        flash('Broken DAG: [{ie.filename}] {ie.stacktrace}'.format(ie=ie), 'error')
    from airflow.plugins_manager import import_errors as plugin_import_errors
    for (filename, stacktrace) in plugin_import_errors.items():
        flash('Broken plugin: [{filename}] {stacktrace}'.format(stacktrace=stacktrace, filename=filename), 'error')
    filter_dag_ids = appbuilder.sm.get_accessible_dag_ids()
    if ('all_dags' not in filter_dag_ids):
        query = query.filter(DM.dag_id.in_(filter_dag_ids))
    query = query.order_by(DM.dag_id)
    start = (current_page * dags_per_page)
    end = (start + dags_per_page)
    dags = query.offset(start).limit(dags_per_page).all()
    num_of_all_dags = query.count()
    num_of_pages = int(math.ceil((num_of_all_dags / float(dags_per_page))))
    auto_complete_data = set()
    for row in query.with_entities(DM.dag_id, DM.owners):
        auto_complete_data.add(row.dag_id)
        auto_complete_data.add(row.owners)
    return self.render('airflow/dags.html', dags=dags, hide_paused=hide_paused, current_page=current_page, search_query=(arg_search_query if arg_search_query else ''), page_size=dags_per_page, num_of_pages=num_of_pages, num_dag_from=(start + 1), num_dag_to=min(end, num_of_all_dags), num_of_all_dags=num_of_all_dags, paging=wwwutils.generate_pages(current_page, num_of_pages, search=arg_search_query, showPaused=(not hide_paused)), auto_complete_data=auto_complete_data, num_runs=num_runs)
