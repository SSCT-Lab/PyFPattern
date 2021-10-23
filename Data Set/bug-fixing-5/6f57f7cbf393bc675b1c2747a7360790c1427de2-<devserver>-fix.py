@click.command()
@click.option('--reload/--no-reload', default=True, help='Autoreloading of python files.')
@click.option('--watchers/--no-watchers', default=True, help='Watch static files and recompile on changes.')
@click.option('--workers/--no-workers', default=False, help='Run asynchronous workers.')
@click.option('--browser-reload/--no-browser-reload', default=False, help='Automatic browser refreshing on webpack builds')
@click.option('--prefix/--no-prefix', default=True, help='Show the service name prefix and timestamp')
@click.option('--styleguide/--no-styleguide', default=False, help='Start local styleguide web server on port 9001')
@click.option('--environment', default='development', help='The environment name.')
@click.argument('bind', default='127.0.0.1:8000', metavar='ADDRESS', envvar='SENTRY_DEVSERVER_BIND')
@log_options()
@configuration
def devserver(reload, watchers, workers, browser_reload, styleguide, prefix, environment, bind):
    'Starts a lightweight web server for development.'
    if (':' in bind):
        (host, port) = bind.split(':', 1)
        port = int(port)
    else:
        host = bind
        port = None
    import os
    os.environ['SENTRY_ENVIRONMENT'] = environment
    from django.conf import settings
    from sentry import options
    from sentry.services.http import SentryHTTPServer
    url_prefix = options.get('system.url-prefix', '')
    parsed_url = urlparse(url_prefix)
    needs_https = ((parsed_url.scheme == 'https') and ((parsed_url.port or 443) > 1024))
    has_https = False
    if needs_https:
        from subprocess import check_output
        try:
            check_output(['which', 'https'])
            has_https = True
        except Exception:
            has_https = False
            from sentry.runner.initializer import show_big_error
            show_big_error(['missing `https` on your `$PATH`, but https is needed', '`$ brew install mattrobenolt/stuff/https`'])
    uwsgi_overrides = {
        'protocol': 'http',
        'worker-reload-mercy': 2,
        'honour-stdin': True,
        'limit-post': (1 << 30),
        'http-chunked-input': True,
        'thunder-lock': False,
        'timeout': 600,
        'harakiri': 600,
    }
    if reload:
        uwsgi_overrides['py-autoreload'] = 1
    daemons = []
    if (watchers and (not browser_reload)):
        daemons += settings.SENTRY_WATCHERS
    if (watchers and browser_reload):
        new_port = (port + 1)
        os.environ['WEBPACK_DEV_PROXY'] = ('%s' % port)
        os.environ['WEBPACK_DEV_PORT'] = ('%s' % (new_port + 1))
        os.environ['SENTRY_DEVSERVER_PORT'] = ('%s' % new_port)
        port = new_port
        daemons += [('jsproxy', ['yarn', 'dev-proxy']), ('webpack', ['yarn', 'dev-server'])]
    if workers:
        if settings.CELERY_ALWAYS_EAGER:
            raise click.ClickException('Disable CELERY_ALWAYS_EAGER in your settings file to spawn workers.')
        daemons += [('worker', ['sentry', 'run', 'worker', '-c', '1', '--autoreload']), ('cron', ['sentry', 'run', 'cron', '--autoreload'])]
    if (needs_https and has_https):
        https_port = six.text_type(parsed_url.port)
        https_host = parsed_url.hostname
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, 0))
        port = s.getsockname()[1]
        s.close()
        bind = ('%s:%d' % (host, port))
        daemons += [('https', ['https', '-host', https_host, '-listen', ((host + ':') + https_port), bind])]
    if daemons:
        uwsgi_overrides['log-format'] = '"%(method) %(uri) %(proto)" %(status) %(size)'
    else:
        uwsgi_overrides['log-format'] = '[%(ltime)] "%(method) %(uri) %(proto)" %(status) %(size)'
    server = SentryHTTPServer(host=host, port=port, workers=1, extra_options=uwsgi_overrides)
    if (not daemons):
        return server.run()
    import sys
    from subprocess import list2cmdline
    from honcho.manager import Manager
    from honcho.printer import Printer
    os.environ['PYTHONUNBUFFERED'] = 'true'
    server.prepare_environment()
    daemons += [('server', ['sentry', 'run', 'web'])]
    if styleguide:
        daemons += [('storybook', ['yarn', 'storybook'])]
    cwd = os.path.realpath(os.path.join(settings.PROJECT_ROOT, os.pardir, os.pardir))
    manager = Manager(Printer(prefix=prefix))
    for (name, cmd) in daemons:
        manager.add_process(name, list2cmdline(cmd), quiet=False, cwd=cwd)
    manager.loop()
    sys.exit(manager.returncode)