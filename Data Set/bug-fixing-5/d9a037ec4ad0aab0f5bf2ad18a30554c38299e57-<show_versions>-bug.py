def show_versions(as_json=False):
    sys_info = get_sys_info()
    deps = [('pandas', (lambda mod: mod.__version__)), ('pytest', (lambda mod: mod.__version__)), ('pip', (lambda mod: mod.__version__)), ('setuptools', (lambda mod: mod.__version__)), ('Cython', (lambda mod: mod.__version__)), ('numpy', (lambda mod: mod.version.version)), ('scipy', (lambda mod: mod.version.version)), ('pyarrow', (lambda mod: mod.__version__)), ('xarray', (lambda mod: mod.__version__)), ('IPython', (lambda mod: mod.__version__)), ('sphinx', (lambda mod: mod.__version__)), ('patsy', (lambda mod: mod.__version__)), ('dateutil', (lambda mod: mod.__version__)), ('pytz', (lambda mod: mod.VERSION)), ('blosc', (lambda mod: mod.__version__)), ('bottleneck', (lambda mod: mod.__version__)), ('tables', (lambda mod: mod.__version__)), ('numexpr', (lambda mod: mod.__version__)), ('feather', (lambda mod: mod.__version__)), ('matplotlib', (lambda mod: mod.__version__)), ('openpyxl', (lambda mod: mod.__version__)), ('xlrd', (lambda mod: mod.__VERSION__)), ('xlwt', (lambda mod: mod.__VERSION__)), ('xlsxwriter', (lambda mod: mod.__version__)), ('lxml', (lambda mod: mod.etree.__version__)), ('bs4', (lambda mod: mod.__version__)), ('html5lib', (lambda mod: mod.__version__)), ('sqlalchemy', (lambda mod: mod.__version__)), ('pymysql', (lambda mod: mod.__version__)), ('psycopg2', (lambda mod: mod.__version__)), ('jinja2', (lambda mod: mod.__version__)), ('s3fs', (lambda mod: mod.__version__)), ('fastparquet', (lambda mod: mod.__version__)), ('pandas_gbq', (lambda mod: mod.__version__)), ('pandas_datareader', (lambda mod: mod.__version__)), ('gcsfs', (lambda mod: mod.__version__))]
    deps_blob = list()
    for (modname, ver_f) in deps:
        try:
            if (modname in sys.modules):
                mod = sys.modules[modname]
            else:
                mod = importlib.import_module(modname)
            ver = ver_f(mod)
            deps_blob.append((modname, ver))
        except ImportError:
            deps_blob.append((modname, None))
    if as_json:
        try:
            import json
        except ImportError:
            import simplejson as json
        j = dict(system=dict(sys_info), dependencies=dict(deps_blob))
        if (as_json is True):
            print(j)
        else:
            with codecs.open(as_json, 'wb', encoding='utf8') as f:
                json.dump(j, f, indent=2)
    else:
        print('\nINSTALLED VERSIONS')
        print('------------------')
        for (k, stat) in sys_info:
            print('{k}: {stat}'.format(k=k, stat=stat))
        print('')
        for (k, stat) in deps_blob:
            print('{k}: {stat}'.format(k=k, stat=stat))