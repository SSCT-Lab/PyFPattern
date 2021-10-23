def configure(ctx, py, yaml, skip_service_validation=False):
    "\n    Given the two different config files, set up the environment.\n\n    NOTE: Will only execute once, so it's safe to call multiple times.\n    "
    global __installed
    if __installed:
        return
    import warnings
    warnings.filterwarnings('default', '', Warning, '^sentry')
    import mimetypes
    for (type, ext) in (('application/json', 'map'), ('application/font-woff', 'woff'), ('application/font-woff2', 'woff2'), ('application/vnd.ms-fontobject', 'eot'), ('application/x-font-ttf', 'ttf'), ('application/x-font-ttf', 'ttc'), ('font/opentype', 'otf'), ('image/svg+xml', 'svg')):
        mimetypes.add_type(type, ('.' + ext))
    from .importer import install
    if (yaml is None):
        if (not os.path.exists(py)):
            if ctx:
                raise click.ClickException("Configuration file does not exist. Use 'sentry init' to initialize the file.")
            raise ValueError(("Configuration file does not exist at '%s'" % click.format_filename(py)))
    elif ((not os.path.exists(yaml)) and (not os.path.exists(py))):
        if ctx:
            raise click.ClickException("Configuration file does not exist. Use 'sentry init' to initialize the file.")
        raise ValueError(("Configuration file does not exist at '%s'" % click.format_filename(yaml)))
    if ((yaml is not None) and os.path.exists(yaml)):
        from sentry.utils.uwsgi import reload_on_change
        reload_on_change(yaml)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'sentry_config'
    install('sentry_config', py, DEFAULT_SETTINGS_MODULE)
    from django.conf import settings
    hasattr(settings, 'INSTALLED_APPS')
    from .initializer import initialize_app, on_configure
    initialize_app({
        'config_path': py,
        'settings': settings,
        'options': yaml,
    }, skip_service_validation=skip_service_validation)
    on_configure({
        'settings': settings,
    })
    __installed = True