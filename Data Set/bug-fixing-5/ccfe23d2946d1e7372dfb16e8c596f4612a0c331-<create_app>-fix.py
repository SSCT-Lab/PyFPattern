def create_app(config=None, session=None, testing=False, app_name='Airflow'):
    global app, appbuilder
    app = Flask(__name__)
    if conf.getboolean('webserver', 'ENABLE_PROXY_FIX'):
        app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=None, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)
    app.secret_key = conf.get('webserver', 'SECRET_KEY')
    app.config.from_pyfile(settings.WEBSERVER_CONFIG, silent=True)
    app.config['APP_NAME'] = app_name
    app.config['TESTING'] = testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = conf.getboolean('webserver', 'COOKIE_SECURE')
    app.config['SESSION_COOKIE_SAMESITE'] = conf.get('webserver', 'COOKIE_SAMESITE')
    if config:
        app.config.from_mapping(config)
    app.json_encoder = AirflowJsonEncoder
    csrf.init_app(app)
    db = SQLA(app)
    from airflow import api
    api.load_auth()
    api.API_AUTH.api_auth.init_app(app)
    cache = Cache(app=app, config={
        'CACHE_TYPE': 'filesystem',
        'CACHE_DIR': '/tmp',
    })
    from airflow.www.blueprints import routes
    app.register_blueprint(routes)
    configure_logging()
    configure_manifest_files(app)
    with app.app_context():
        from airflow.www.security import AirflowSecurityManager
        security_manager_class = (app.config.get('SECURITY_MANAGER_CLASS') or AirflowSecurityManager)
        if (not issubclass(security_manager_class, AirflowSecurityManager)):
            raise Exception("Your CUSTOM_SECURITY_MANAGER must now extend AirflowSecurityManager,\n                 not FAB's security manager.")
        appbuilder = AppBuilder(app, (db.session if (not session) else session), security_manager_class=security_manager_class, base_template='appbuilder/baselayout.html')

        def init_views(appbuilder):
            from airflow.www import views
            appbuilder.add_view_no_menu(views.Airflow())
            appbuilder.add_view_no_menu(views.DagModelView())
            appbuilder.add_view_no_menu(views.ConfigurationView())
            appbuilder.add_view_no_menu(views.VersionView())
            appbuilder.add_view(views.DagRunModelView, 'DAG Runs', category='Browse', category_icon='fa-globe')
            appbuilder.add_view(views.JobModelView, 'Jobs', category='Browse')
            appbuilder.add_view(views.LogModelView, 'Logs', category='Browse')
            appbuilder.add_view(views.SlaMissModelView, 'SLA Misses', category='Browse')
            appbuilder.add_view(views.TaskInstanceModelView, 'Task Instances', category='Browse')
            appbuilder.add_link('Configurations', href='/configuration', category='Admin', category_icon='fa-user')
            appbuilder.add_view(views.ConnectionModelView, 'Connections', category='Admin')
            appbuilder.add_view(views.PoolModelView, 'Pools', category='Admin')
            appbuilder.add_view(views.VariableModelView, 'Variables', category='Admin')
            appbuilder.add_view(views.XComModelView, 'XComs', category='Admin')
            appbuilder.add_link('Documentation', href='https://airflow.apache.org/', category='Docs', category_icon='fa-cube')
            appbuilder.add_link('GitHub', href='https://github.com/apache/airflow', category='Docs')
            appbuilder.add_link('Version', href='/version', category='About', category_icon='fa-th')

            def integrate_plugins():
                'Integrate plugins to the context'
                from airflow.plugins_manager import flask_appbuilder_views, flask_appbuilder_menu_links
                for v in flask_appbuilder_views:
                    log.debug('Adding view %s', v['name'])
                    appbuilder.add_view(v['view'], v['name'], category=v['category'])
                for ml in sorted(flask_appbuilder_menu_links, key=(lambda x: x['name'])):
                    log.debug('Adding menu link %s', ml['name'])
                    appbuilder.add_link(ml['name'], href=ml['href'], category=ml['category'], category_icon=ml['category_icon'])
            integrate_plugins()

        def init_plugin_blueprints(app):
            from airflow.plugins_manager import flask_blueprints
            for bp in flask_blueprints:
                log.debug('Adding blueprint %s:%s', bp['name'], bp['blueprint'].import_name)
                app.register_blueprint(bp['blueprint'])
        init_views(appbuilder)
        init_plugin_blueprints(app)
        security_manager = appbuilder.sm
        security_manager.sync_roles()
        from airflow.www.api.experimental import endpoints as e
        if app.config['TESTING']:
            import importlib
            importlib.reload(e)
        app.register_blueprint(e.api_experimental, url_prefix='/api/experimental')

        @app.context_processor
        def jinja_globals():
            return {
                'hostname': socket.getfqdn(),
                'navbar_color': conf.get('webserver', 'NAVBAR_COLOR'),
            }

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            settings.Session.remove()
    return (app, appbuilder)