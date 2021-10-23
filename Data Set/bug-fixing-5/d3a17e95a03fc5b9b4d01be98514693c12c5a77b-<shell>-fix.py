@cli_utils.action_logging
def shell(args):
    'Run a shell that allows to access metadata database'
    url = settings.engine.url
    print(('DB: ' + repr(url)))
    if (url.get_backend_name() == 'mysql'):
        with NamedTemporaryFile(suffix='my.cnf') as f:
            content = textwrap.dedent(f'''
                [client]
                host     = {url.host}
                user     = {url.username}
                password = {(url.password or '')}
                port     = {(url.port or '')}
                database = {url.database}
                ''').strip()
            f.write(content.encode())
            f.flush()
            subprocess.Popen(['mysql', f'--defaults-extra-file={f.name}']).wait()
    elif (url.get_backend_name() == 'sqlite'):
        subprocess.Popen(['sqlite3', url.database]).wait()
    elif (url.get_backend_name() == 'postgresql'):
        env = os.environ.copy()
        env['PGHOST'] = (url.host or '')
        env['PGPORT'] = (url.port or '')
        env['PGUSER'] = (url.username or '')
        env['PGPASSWORD'] = (url.password or '')
        env['PGDATABASE'] = url.database
        subprocess.Popen(['psql'], env=env).wait()
    else:
        raise AirflowException(f'Unknown driver: {url.drivername}')