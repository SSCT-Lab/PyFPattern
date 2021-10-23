

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
        except Exception:
            return None
    try:
        unwrap = inspect.unwrap
    except AttributeError:
        pass
    else:
        obj = unwrap(obj)
    try:
        fn = inspect.getsourcefile(obj)
    except Exception:
        fn = None
    if (not fn):
        return None
    try:
        (source, lineno) = inspect.getsourcelines(obj)
    except Exception:
        lineno = None
    if lineno:
        linespec = ('#L%d-L%d' % (lineno, ((lineno + len(source)) - 1)))
    else:
        linespec = ''
    fn = relpath(fn, start=dirname(numpy.__file__))
    if ('dev' in numpy.__version__):
        return ('https://github.com/numpy/numpy/blob/master/numpy/%s%s' % (fn, linespec))
    else:
        return ('https://github.com/numpy/numpy/blob/v%s/numpy/%s%s' % (numpy.__version__, fn, linespec))
