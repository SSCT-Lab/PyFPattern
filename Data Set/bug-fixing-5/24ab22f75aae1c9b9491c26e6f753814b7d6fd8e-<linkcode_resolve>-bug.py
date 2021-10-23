def linkcode_resolve(domain, info):
    '\n    Determine the URL corresponding to Python object\n    '
    if (domain != 'py'):
        return None
    modname = info['module']
    fullname = info['fullname']
    submod = sys.modules.get(modname)
    if (submod is None):
        return None
    obj = submod
    for part in fullname.split('.'):
        try:
            obj = getattr(obj, part)
        except:
            return None
    try:
        fn = inspect.getsourcefile(obj)
    except:
        fn = None
    if (not fn):
        return None
    try:
        (source, lineno) = inspect.getsourcelines(obj)
    except:
        lineno = None
    if lineno:
        linespec = '#L{:d}-L{:d}'.format(lineno, ((lineno + len(source)) - 1))
    else:
        linespec = ''
    fn = os.path.relpath(fn, start=os.path.dirname(pandas.__file__))
    if ('+' in pandas.__version__):
        return 'http://github.com/pandas-dev/pandas/blob/master/pandas/{}{}'.format(fn, linespec)
    else:
        return 'http://github.com/pandas-dev/pandas/blob/v{}/pandas/{}{}'.format(pandas.__version__, fn, linespec)